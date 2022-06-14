import contextlib
import dataclasses
from typing import Optional, Tuple

from magma.bits import BitsMeta
from magma.clock import ClockTypes
from magma.circuit import Circuit, CircuitBuilder
from magma.conversions import as_bits
from magma.definition_context import definition_context_manager
from magma.digital import DigitalMeta
from magma.generator import Generator2
from magma.inline_verilog import inline_verilog
from magma.interface import IO
from magma.passes.group import GrouperBase, InstanceCollection
from magma.primitives.mux import infer_mux_type
from magma.ref import InstRef, get_ref_defn, get_ref_inst
from magma.t import Kind, Type, In, Out
from magma.type_utils import type_to_sanitized_string
from magma.value_utils import make_selector


@dataclasses.dataclass(frozen=True)
class _CompileGuardState:
    ckt: CircuitBuilder
    ctx_mgr: contextlib.AbstractContextManager


class _Grouper(GrouperBase):
    def __init__(self, instances: InstanceCollection, builder: CircuitBuilder):
        super().__init__(instances)
        self._builder = builder
        self._port_index = 0

    def _visit_input_connection(self, driver: Type, drivee: Type):
        new_port_name = self._new_port_name()
        T = type(driver).undirected_t
        self._builder._add_port(new_port_name, In(T))
        new_port = self._builder._port(new_port_name)
        drivee.unwire(driver)
        drivee @= new_port
        external = getattr(self._builder, new_port_name)
        external @= driver

    def _visit_output_connection(self, driver: Type, drivee: Type):
        raise NotImplementedError()

    def _visit_undriven_port(self, port: Type):
        # TODO(rsetaluri): Alert (raise or log) in this case; undriven port.
        if not isinstance(port, ClockTypes):
            return
        T = type(port).undirected_t
        # TODO(rsetaluri): Ensure that we don't add multiple clock types.
        name = str(port.name)
        self._builder._add_port(name, In(T))

    def _new_port_name(self):
        name = f"port_{self._port_index}"
        self._port_index += 1
        return name


class _CompileGuardBuilder(CircuitBuilder):
    def __init__(self, name, cond, type):
        super().__init__(name)
        self._cond = cond
        self._system_types_added = set()
        if type not in {"defined", "undefined"}:
            raise ValueError(f"Unexpected compile guard type: {type}")
        self._set_inst_attr(
            "coreir_metadata",
            {"compile_guard": {"condition_str": cond, "type": type}}
        )
        self._pre_finalized = False

    def pre_finalize(self):
        if self._pre_finalized:
            raise Exception("Can not call pre_finalize multiple times")
        grouper = _Grouper(self._instances, self)
        grouper.run()
        self._pre_finalized = True


class _CompileGuard:
    __index = 0

    def __init__(self, cond: str,
                 defn_name: Optional[str],
                 inst_name: Optional[str],
                 type: Optional[str] = "defined"):
        self._cond = cond
        self._defn_name = defn_name
        self._inst_name = inst_name
        self._state = None
        self._type = type

    @staticmethod
    def _new_name():
        index = _CompileGuard.__index
        _CompileGuard.__index += 1
        return f"CompileGuardCircuit_{index}"

    def __enter__(self):
        if self._state is not None:
            raise Exception("Can not enter compile guard multiple times")
        assert self._state is None
        if self._defn_name is None:
            self._defn_name = _CompileGuard._new_name()
        if self._state is None:
            ckt = _CompileGuardBuilder(self._defn_name, self._cond, self._type)
            if self._inst_name is None:
                ckt.set_instance_name(self._inst_name)
            ctx_mgr = definition_context_manager(ckt._context)
            self._state = _CompileGuardState(ckt, ctx_mgr)
        self._state.ctx_mgr.__enter__()

    def __exit__(self, typ, value, traceback):
        self._state.ctx_mgr.__exit__(typ, value, traceback)
        self._state.ckt.pre_finalize()


def compile_guard(cond: str,
                  defn_name: Optional[str] = None,
                  inst_name: Optional[str] = None,
                  type: Optional[str] = "defined"):
    return _CompileGuard(cond, defn_name, inst_name, type)


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
