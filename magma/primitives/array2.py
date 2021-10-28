"""
Monkey patched functions to avoid circular dependencies in Array2 definitions
"""
from functools import lru_cache

from magma.interface import IO
from magma.t import In, Out
from magma.circuit import coreir_port_mapping, CircuitBuilder, builder_method
from magma.generator import Generator2
from magma.array import Array2


class Index(Generator2):
    def __init__(self, T, i):
        self.io = IO(I=In(T), O=Out(T.T))
        self.coreir_genargs = {"t": T, "i": i}
        self.coreir_name = "getArrT"
        self.coreir_lib = "mantle"
        self.renamed_ports = coreir_port_mapping


# Array2._make_get = lambda self, index: Index(type(self), index)


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


# Array2._make_slice = _make_slice


class Lift(Generator2):
    def __init__(self, T):
        self.io = IO(I=In(T), O=Out(Array2[1, T]))
        self.coreir_genargs = {"t": Array2[1, In(T)]}
        self.coreir_name = "liftArrT"
        self.coreir_lib = "mantle"
        self.renamed_ports = coreir_port_mapping


def _make_lift(self):
    return Lift(type(self).T)


Array2._make_lift = _make_lift


class Slices(Generator2):
    def __init__(self, T, slices):
        self.renamed_ports = coreir_port_mapping
        ports = {"I": In(T)}
        for i, slice in enumerate(slices):
            ports[f"O{i}"] = Out(T[slice[0] - slice[1], T.T])
            self.renamed_ports[f"O{i}"] = f"out{i}"
        self.io = IO(**ports)
        self.coreir_genargs = {"t": Out(T),
                               "slices": list(list(s) for s in slices)}
        self.coreir_name = "slicesArrT"
        self.coreir_lib = "mantle"
        self.combinational = True


def _make_slices(self, slices):
    return Slices(type(self), slices)


Array2._make_slices = _make_slices


class SlicesBuilder(CircuitBuilder):
    def __init__(self, I):
        super().__init__("SlicesBuilder")
        self._slices = {}
        self.T = type(I)
        self._add_port("in", In(self.T))
        getattr(self, "in").wire(I)

    @lru_cache()
    def _make_type(self, n):
        return Array2[n, self.T.T]

    @builder_method
    def add(self, start, stop):
        if (stop, start) not in self._slices:
            name = f"out{len(self._slices)}"
            typ = self._make_type(stop - start)
            self._add_port(name, typ)
            self._slices[(stop, start)] = getattr(self, name)
        return self._slices[(stop, start)]

    def _finalize(self):
        slices_param = list(list(s) for s in self._slices.keys())
        self._set_definition_attr("coreir_genargs",
                                  {"t": Out(self.T), "slices": slices_param})
        self._set_definition_attr("coreir_name", "slicesArrT")
        self._set_definition_attr("coreir_lib", "mantle")
        self._set_definition_attr("combinational", True)


Array2._make_slices_builder = lambda self: SlicesBuilder(self)


class GetsBuilder(CircuitBuilder):
    def __init__(self, I):
        super().__init__("GetsBuilder")
        self._gets = {}
        self.T = type(I)
        self._add_port("in", In(self.T))
        getattr(self, "in").wire(I)

    @builder_method
    def add(self, idx):
        if idx not in self._gets:
            name = f"out{len(self._gets)}"
            self._add_port(name, self.T.T)
            self._gets[idx] = getattr(self, name)
        return self._gets[idx]

    def _finalize(self):
        gets_param = list(self._gets.keys())
        self._set_definition_attr("coreir_genargs",
                                  {"t": Out(self.T), "gets": gets_param})
        self._set_definition_attr("coreir_name", "getsArrT")
        self._set_definition_attr("coreir_lib", "mantle")
        self._set_definition_attr("combinational", True)


Array2._make_gets_builder = lambda self: GetsBuilder(self)
