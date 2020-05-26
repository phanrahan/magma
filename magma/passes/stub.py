from typing import Iterable

from magma.circuit import CircuitKind
from magma.passes.passes import CircuitPass


def _drive_if_undriven_input(port):
    if port.is_mixed():
        for p in port:
            _drive_if_undriven_input(p)
        return
    # NOTE(rsetaluri): This may override previously wired inputs, resulting in a
    # warning. In this case, this warning is benign.
    if port.is_input():
        port.undriven()


class StubPass(CircuitPass):
    def __init__(self, main: CircuitKind, stubs: Iterable[CircuitKind]):
        super().__init__(main)
        self._stubs = set(stubs)

    def __call__(self, cls):
        try:
            self._stubs.remove(cls)
        except KeyError:
            return  # @cls not in stubs, don't need to do anything
        with cls.open():
            for port in cls.interface.ports.values():
                _drive_if_undriven_input(port)
