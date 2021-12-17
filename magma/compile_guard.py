import dataclasses
from typing import Optional, Tuple

from magma.bits import BitsMeta
from magma.clock import Clock
from magma.circuit import Circuit, CircuitBuilder, DefinitionContextManager
from magma.conversions import as_bits
from magma.digital import DigitalMeta
from magma.generator import Generator2
from magma.inline_verilog import inline_verilog
from magma.interface import IO
from magma.primitives.mux import infer_mux_type
from magma.ref import (
    AnonRef, ArrayRef, DefnRef, InstRef, TupleRef, TempNamedRef)
from magma.t import Kind, In, Out
from magma.type_utils import type_to_sanitized_string
from magma.value_utils import make_selector


def _get_top_ref(ref):
    if isinstance(ref, TupleRef):
        # TODO(rsetaluri): Fix port name collision.
        return _get_top_ref(ref.tuple.name)
    if isinstance(ref, ArrayRef):
        # TODO(rsetaluri): Fix port name collision.
        return _get_top_ref(ref.array.name)
    return ref


class CompileGuardUndrivenTemporaryError(RuntimeError):
    pass


@dataclasses.dataclass(frozen=True)
class _CompileGuardState:
    ckt: CircuitBuilder
    ctx_mgr: DefinitionContextManager


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
        self._port_index = 0
        self._pre_finalized = False

    def _new_port_name(self):
        name = f"port_{self._port_index}"
        self._port_index += 1
        return name

    def _rewire_input(self, port, value):
        new_port_name = self._new_port_name()
        T = type(value).undirected_t
        self._add_port(new_port_name, In(T))
        new_port = self._port(new_port_name)
        port.unwire(value)
        port @= new_port
        external = getattr(self, new_port_name)
        external @= value

    def pre_finalize(self):
        if self._pre_finalized:
            raise Exception("Can not call pre_finalize multiple times")
        for inst in self._instances:
            self._process_instance(inst)
        self._pre_finalized = True

    def _process_instance(self, inst):
        # TODO(rseatluri,leonardt): Handle mixed types and in-outs.
        for port in inst.interface.inputs(include_clocks=True):
            self._process_input(port)
        for port in inst.interface.outputs():
            self._process_output(port)

    def _is_external(self, value):
        # A value is external if it is either a port of the containing
        # definition, or a port of an instance contained in the containing
        # definition. To compute this we consider three cases:
        #   (1) @value is a port of a definition. In this case we assume that
        #       the definition is the containing definition (this not being the
        #       case is an error, and will be caught anyway downstream).
        #   (2) @value is a port of an instance. If the instance is contained
        #       inside *ourself*, then @value is *not* external. Otherwise, we
        #       assume @value is external (again, if the instance is not
        #       contained in the containing definition, an error will be raised
        #       downstream anyway).
        #   (3) @value is a temporary. If @value itself is not driven, then we
        #       do not have sufficient information to determine externality, and
        #       raise an error. Otherwise, we recursively call _is_external on
        #       the driver of @value.
        top_ref = _get_top_ref(value.name)
        if isinstance(top_ref, DefnRef):
            return True
        if isinstance(top_ref, InstRef):
            return top_ref.inst not in self._instances
        if isinstance(top_ref, (TempNamedRef, AnonRef)):
            if not value.driven():
                raise CompileGuardUndrivenTemporaryError()
            return self._is_external(value.value())
        return False

    def _process_output(self, port):
        drivees = sum(as_bits(port).driving(), [])
        external_drivees = list(filter(self._is_external, drivees))
        if not external_drivees:
            return
        new_port_name = self._new_port_name()
        T = type(port).undirected_t
        self._add_port(new_port_name, Out(T))
        new_port = self._port(new_port_name)
        new_port @= port
        external = getattr(self, new_port_name)
        for drivee in external_drivees:
            old_driver = drivee.value()
            drivee.unwire(old_driver)
            selector = make_selector(old_driver)
            new_driver = selector.select(external)
            drivee @= new_driver

    def _process_input(self, port):
        # There are 4 total cases here:
        #   (1) @port is undriven, in which case we delegate to
        #       _process_undriven_input.
        #   (2) @port is driven by @driver:
        #       (a) @driver is a constant, in which case we do not have to do
        #           anything and can leave the driver as is.
        #       (b) @driver is 'external' (see _is_external for a definition),
        #           in which case we need to rewire the input through a new port
        #           (ala boring).
        #       (c) @driver is 'internal', in which case we again need to do
        #           nothing. Because _is_external is exhaustive, we can simply
        #           assume in the implicit else clause that we don't need to do
        #           anything.
        if not port.driven():
            self._process_undriven_input(port)
            return
        driver = port.value()
        if driver.const():
            return
        if self._is_external(driver):
            self._rewire_input(port, driver)
            return

    def _process_undriven_input(self, port):
        # TODO(rsetaluri): Add other system types.
        if not isinstance(port, Clock):
            return
        T = type(port).undirected_t
        if T in self._system_types_added:
            return
        name = str(port.name)
        self._add_port(name, In(T))
        self._system_types_added.add(T)


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
            ctx_mgr = DefinitionContextManager(ckt._context)
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
