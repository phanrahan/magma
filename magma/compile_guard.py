import dataclasses
from typing import List, Optional

from magma.array import Array
from magma.bits import Bits
from magma.clock import Clock
from magma.circuit import Circuit, CircuitBuilder, _DefinitionContextManager
from magma.digital import Digital
from magma.ref import AnonRef, ArrayRef, DefnRef, InstRef, TupleRef
from magma.t import In
from magma.tuple import Tuple


@dataclasses.dataclass(frozen=True)
class _CompileGuardState:
    ckt: CircuitBuilder
    ctx_mgr: _DefinitionContextManager


class _CompileGuardBuilder(CircuitBuilder):
    def __init__(self, name, cond):
        super().__init__(name)
        self._cond = cond
        self._system_types_added = set()
        self._set_inst_attr("coreir_metadata", {"compile_guard": cond})
        self._port_index = 0
        self._pre_finalized = False

    def _new_port_name(self):
        name = f"port_{self._port_index}"
        self._port_index += 1
        return name

    def _rewire(self, port, value):
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
        for port in inst.interface.inputs(include_clocks=True):
            self._process_port(port)

    def _process_port(self, port, ref=None, kwargs=None):
        value = port.value()
        if ref is None:
            if value is None:
                self._process_undriven(port)
                return
            ref = value.name
        if isinstance(ref, AnonRef):
            if value.const():
                return
            # TODO(rsetaluri): Implement valid anon. values.
            raise NotImplementedError()
        if isinstance(ref, DefnRef):
            self._rewire(port, value)
            return
        if isinstance(ref, InstRef):
            internal = any(ref.inst is inst for inst in self._instances)
            if internal:
                return
            self._rewire(port, value)
            return
        if isinstance(ref, TupleRef):
            # TODO(rsetaluri): Fix port name collision.
            self._process_port(port, ref=ref.tuple.name)
            return
        if isinstance(ref, ArrayRef):
            # TODO(rsetaluri): Fix port name collision.
            self._process_port(port, ref=ref.array.name)
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
                 inst_name: Optional[str]):
        self._cond = cond
        self._defn_name = defn_name
        self._inst_name = inst_name
        self._state = None

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
            ckt = _CompileGuardBuilder(self._defn_name, self._cond)
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
                  inst_name: Optional[str] = None):
    return _CompileGuard(cond, defn_name, inst_name)
