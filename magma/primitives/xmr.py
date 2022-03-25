from magma.generator import Generator2
from magma.interface import IO
from magma.t import Kind, In, Out
from magma.view import PortView


class XMR(m.Generator2):
    def __init__(self, value: PortView):
        self.T = T = type(value)._to_magma_()
        self.io = io = IO(I=In(T), O=Out(T))
        self.primitive = True

        self._value = value

    @property
    def value(self) -> PortView:
        return self._value
