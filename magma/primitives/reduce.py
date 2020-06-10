import operator
import functools

from hwtypes import BitVector

from magma.bit import Bit
from magma.bits import Bits
from magma.circuit import coreir_port_mapping, IO
from magma.generator import Generator2
from magma.t import In, Out


def _reduce_factory(coreir_name, operator):
    class Reduce(Generator2):
        def __init__(self, width: int):
            self.io = IO(I=In(Bits[width]), O=Out(Bit))
            self.coreir_lib = "coreir"
            self.coreir_name = coreir_name
            self.name = f"coreir_{coreir_name}_{width}"
            self.coreir_genargs = {"width": width}
            self.renamed_ports = coreir_port_mapping
            self.primitive = True
            self.stateful = False

            def simulate(self, value_store, state_store):
                I = BitVector[width](value_store.get_value(self.I))
                O = functools.reduce(operator, I.bits())
                value_store.set_value(self.O, O)

            self.simulate = simulate
    return Reduce


_OP_MAP = {
    operator.and_: _reduce_factory("andr", operator.and_),
    operator.or_: _reduce_factory("orr", operator.or_),
    operator.xor: _reduce_factory("xorr", operator.xor)
}


def reduce(operator, bits: Bits):
    if not isinstance(bits, Bits):
        raise TypeError("m.reduce only works with Bits")
    if operator not in _OP_MAP:
        raise ValueError(f"{operator} not supported")
    return _OP_MAP[operator](len(bits))()(bits)
