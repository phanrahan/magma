import dataclasses
from typing import List, Optional

from magma.array import Array
from magma.bits import Bits
from magma.clock import Clock
from magma.circuit import Circuit, CircuitBuilder, _DefinitionContextManager
from magma.conversions import as_bits
from magma.digital import Digital
from magma.ref import AnonRef, ArrayRef, DefnRef, InstRef, TupleRef
from magma.t import In, Out
from magma.tuple import Tuple
from magma.value_utils import make_selector


def _get_top_ref(ref):
    if isinstance(ref, TupleRef):
        # TODO(rsetaluri): Fix port name collision.
        return _get_top_ref(ref.tuple.name)
    if isinstance(ref, ArrayRef):
        # TODO(rsetaluri): Fix port name collision.
        return _get_top_ref(ref.array.name)
    return ref


@dataclasses.dataclass(frozen=True)
class _CompileGuardState:
    ckt: CircuitBuilder
    ctx_mgr: _DefinitionContextManager


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
        top_ref = _get_top_ref(value.name)
        if isinstance(top_ref, DefnRef):
            return True
        if isinstance(top_ref, InstRef):
            return top_ref.inst not in self._instances
        if isinstance(top_ref, AnonRef):
            # TODO(rsetaluri): Implement valid anon. values.
            raise NotImplementedError()
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

    def _process_input(self, port, ref=None, kwargs=None):
        value = port.value()
        if ref is None:
            if value is None:
                self._process_undriven(port)
                return
            ref = value.name
        if value.const():
            return
        if self._is_external(value):
            self._rewire_input(port, value)
            return
        ref = _get_top_ref(ref)
        if isinstance(ref, InstRef):
            # Internal instance driver is okay
            assert not self._is_external(value)
            return
        # TODO(rsetaluri): Do the rest of these.
        raise NotImplementedError(ref, type(ref))

    def _process_undriven(self, port):
        # TODO(rsetaluri): Add other system types
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
            ctx_mgr = _DefinitionContextManager(ckt._context)
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
