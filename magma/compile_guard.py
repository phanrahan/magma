import contextlib
import itertools
from typing import Dict, Optional, Tuple, Union

from magma.bits import BitsMeta
from magma.clock import ClockTypes
from magma.circuit import CircuitKind, AnonymousCircuitType, CircuitBuilder
from magma.digital import DigitalMeta
from magma.generator import Generator2
from magma.interface import IO
from magma.logging import root_logger
from magma.passes.group import GrouperBase, InstanceCollection
from magma.primitives.mux import infer_mux_type
from magma.t import Kind, Type, In, Out
from magma.type_utils import type_to_sanitized_string


_logger = root_logger().getChild("compile_guard")


class _Grouper(GrouperBase):
    def __init__(self, instances: InstanceCollection, builder: CircuitBuilder):
        super().__init__(instances)
        self._builder = builder
        self._port_index = 0
        self._clock_types = set()

    def _visit_input_connection(self, _: Type, drivee: Type):
        # NOTE(rsetaluri): Since the driver might be traced (i.e. not an
        # immediate driver), we disregard it and grab the immediate driver
        # (value() vs. trace()).
        driver = drivee.value()
        new_port = self._builder.add_port(In(type(driver)))
        drivee.rewire(new_port)
        external = getattr(self._builder, new_port.name.name)
        external @= driver

    def _visit_output_connection(self, driver: Type, drivee: Type):
        raise TypeError(
            "Driving values outside of compile guard not supported. Use "
            "m.compile_guard_select() instead."
        )

    def _visit_undriven_port(self, port: Type):
        # For undriven clock types, we simply lift the port *but do not connect
        # it* since we expect auto-wiring to do this for us (in fact, this is
        # why the port is undriven in the first place). For non-clock types, we
        # simply log a debug message and allow the downstream circuit pipeline
        # to handle the undriven port.
        if not isinstance(port, ClockTypes):
            _logger.debug(f"found undriven port: {port}")
            return
        T = type(port).undirected_t
        if T in self._clock_types:
            return  # only add at most one port for each clock type
        self._clock_types.add(T)
        self._builder.add_port(In(T))


class _CompileGuardBuilder(CircuitBuilder):
    __default_defn_name_counter = itertools.count()

    @staticmethod
    def _make_default_defn_name() -> str:
        counter = next(_CompileGuardBuilder.__default_defn_name_counter)
        return f"CompileGuardCircuit_{counter}"

    def __init__(self, name: Optional[str], cond: str, type: str):
        if name is None:
            name = _CompileGuardBuilder._make_default_defn_name()
        super().__init__(name)
        self._cond = cond
        self._system_types_added = set()
        if type not in {"defined", "undefined"}:
            raise ValueError(f"Unexpected compile guard type: {type}")
        metadata = {"condition_str": cond, "type": type}
        self._set_inst_attr("coreir_metadata", {"compile_guard": metadata})
        self._set_definition_attr("_compile_guard_", metadata)
        self._num_ports = itertools.count()

    def add_port(self, T: Kind, name: Optional[str] = None) -> Type:
        if name is None:
            name = self._new_port_name()
        return self._add_port(name, T)

    def instances(self) -> InstanceCollection:
        return self._instances.copy()

    def open(self):
        return self._open()

    def _new_port_name(self) -> str:
        return f"port_{next(self._num_ports)}"


def get_compile_guard_data(
        inst_or_defn: Union[AnonymousCircuitType, CircuitKind]
) -> Optional[Dict]:
    """Returns compile guard metadata (compile guard condition string and type
    (ifdef or ifndef)) attached to an instance or definition, or None if it is
    not a compile guarded module.
    """
    if isinstance(inst_or_defn, AnonymousCircuitType):
        coreir_metadata = getattr(inst_or_defn, "coreir_metadata", {})
        return coreir_metadata.get("compile_guard", None)
    if isinstance(inst_or_defn, CircuitKind):
        return getattr(inst_or_defn, "_compile_guard_", None)
    raise TypeError(inst_or_defn)


def _make_builder(
        cond: str,
        defn_name: Optional[str],
        inst_name: Optional[str],
        type: str
) -> _CompileGuardBuilder:
    builder = _CompileGuardBuilder(defn_name, cond, type)
    if inst_name is not None:
        builder.set_instance_name(inst_name)
    return builder


@contextlib.contextmanager
def compile_guard(
        cond: str,
        defn_name: Optional[str] = None,
        inst_name: Optional[str] = None,
        type: str = "defined",
):
    builder = _make_builder(cond, defn_name, inst_name, type)
    with builder.open() as f:
        yield f
    grouper = _Grouper(builder.instances(), builder)
    grouper.run()


def _is_simple_type(T: Kind) -> bool:
    return isinstance(T, (DigitalMeta, BitsMeta))


class _CompileGuardSelect(Generator2):
    def __init__(self, T: Kind, keys: Tuple[str]):
        # NOTE(rsetaluri): We need to add this check because the implementation
        # of this generator emits verilog directly, and thereby requires that no
        # transformations happen to the port names/types. If the type is not
        # "simple" (i.e. Bit or Bits[N]) then the assumption breaks down and
        # this implementation will not work.
        if not _is_simple_type(T):
            raise TypeError(f"Unsupported type: {T}")
        num_keys = len(keys)
        assert num_keys > 1
        self.io = IO(**{f"I{i}": In(T) for i in range(num_keys)}, O=Out(T))
        self.verilog = ""
        for i, key in enumerate(keys):
            if i == 0:
                stmt = f"`ifdef {key}"
            elif key == "default":
                assert i == (num_keys - 1)
                stmt = "`else"
            else:
                stmt = f"`elsif {key}"
            self.verilog += f"""\
{stmt}
    assign O = I{i};
"""
        self.verilog += "`endif"
        T_str = type_to_sanitized_string(T)
        self.name = f"CompileGuardSelect_{T_str}_{'_'.join(keys)}"


def compile_guard_select(**kwargs):
    try:
        default = kwargs.pop("default")
    except KeyError:
        raise ValueError("Expected default argument") from None
    if not (len(kwargs) > 1):
        raise ValueError("Expected at least one key besides default")
    # We rely on insertion order to make the default the last element for the
    # generated if/elif/else code.
    kwargs["default"] = default
    T, _ = infer_mux_type(list(kwargs.values()))
    Select = _CompileGuardSelect(T, tuple(kwargs.keys()))
    return Select()(*kwargs.values())
