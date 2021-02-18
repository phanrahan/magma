import dataclasses
from typing import List

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
        self._system_types_added = {}
        self._set_inst_attr("coreir_metadata", {"compile_guard": cond})

    def _rewire(self, port, value):
        new_port_name = f"__{id(port.name.inst)}_{port.name.name}"
        T = type(value).undirected_t
        self._add_port(new_port_name, In(T))
        new_port = self._port(new_port_name)
        port.unwire(value)
        port @= new_port
        external = getattr(self, new_port_name)
        external @= value

    def _pre_finalize(self):
        for inst in self._instances:
            self._process_instance(inst)

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
        self._system_types_added[T] = name


class _CompileGuard:
    __index = 0

    def __init__(self, cond: str):
        self._cond = cond
        self._state = None

    @staticmethod
    def _new_name():
        index = _CompileGuard.__index
        _CompileGuard.__index += 1
        return f"IfDefCircuit_{index}"

    def __enter__(self):
        if self._state is not None:
            raise Exception("Can not enter compile guard multiple times")
        assert self._state is None
        if self._state is None:
            name = _CompileGuard._new_name()
            ckt = _CompileGuardBuilder(name, self._cond)
            ctx_mgr = _DefinitionContextManager(ckt._context)
            self._state = _CompileGuardState(ckt, ctx_mgr)
        self._state.ctx_mgr.__enter__()

    def __exit__(self, typ, value, traceback):
        self._state.ctx_mgr.__exit__(typ, value, traceback)
        self._state.ckt._pre_finalize()
        # TODO(rsetaluri): Handle inline verilog.


def compile_guard(cond: str):
    return _CompileGuard(cond)
