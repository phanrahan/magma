"""
Monkey patched functions to avoid circular dependencies in Array2 definitions
"""
from magma.interface import IO
from magma.t import In, Out
from magma.circuit import coreir_port_mapping
from magma.generator import Generator2
from magma.array import Array2


class Index(Generator2):
    def __init__(self, T, i):
        self.io = IO(I=In(T), O=Out(T.T))
        self.coreir_genargs = {"t": T, "i": i}
        self.coreir_name = "getArrT"
        self.coreir_lib = "mantle"
        self.renamed_ports = coreir_port_mapping


Array2._make_get = lambda self, index: Index(type(self), index)


class Slice(Generator2):
    def __init__(self, T, start, stop):
        self.io = IO(I=In(T), O=Out(Array2[stop - start, T.T]))
        self.coreir_genargs = {"t": T, "hi": stop,
                               "lo": start}
        self.coreir_name = "sliceArrT"
        self.coreir_lib = "mantle"
        self.renamed_ports = coreir_port_mapping


def _make_slice(self, start, stop=None):
    if stop is None:
        stop = start + 1
    return Slice(type(self), start, stop)


Array2._make_slice = _make_slice
