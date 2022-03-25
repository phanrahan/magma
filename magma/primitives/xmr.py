from magma.generator import Generator2
from magma.interface import IO
from magma.t import Kind, In, Out
from magma.view import PortView


class XMRSink(Generator2):
    def __init__(self, value: PortView):
        self.T = T = type(value)._to_magma_()
        self.io = io = IO(I=In(T))
        self.primitive = True

        self._value = value

    @property
    def value(self) -> PortView:
        return self._value


class XMRSource(Generator2):
    def __init__(self, value: PortView):
        self.T = T = type(value)._to_magma_()
        self.io = io = IO(O=Out(T))
        self.primitive = True

        self._value = value

    @property
    def value(self) -> PortView:
        return self._value
