from magma.generator import Generator2
from magma.interface import IO
from magma.t import Kind, In, Out
from magma.view import PortView


class _XMRPrimitiveBase(Generator2):
    def __init__(self, value: PortView):
        self.T = T = type(value)._to_magma_()
        self.io = io = IO(**type(self).make_ports(T))
        self.primitive = True

        self._value = value

    @property
    def value(self) -> PortView:
        return self._value


class XMRSink(_XMRPrimitiveBase):
    @staticmethod
    def make_ports(T: Kind):
        return {"I": In(T)}


class XMRSource(_XMRPrimitiveBase):
    @staticmethod
    def make_ports(T: Kind):
        return {"O": Out(T)}
