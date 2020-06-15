from typing import Tuple

from hwtypes import BitVector

from magma.bit import Bit
from magma.bits import Bits
from magma.bitutils import clog2
from magma.braid import fork
from magma.circuit import coreir_port_mapping
from magma.conversions import from_bits, as_bits
from magma.interface import IO
from magma.t import Kind, In, Out
from magma.generator import Generator2


class _CoreIRLUT(Generator2):
    """
    Internally used generator for CoreIR LUT primitive
    """

    def __init__(self, contents: BitVector):
        n = clog2(len(contents))
        self.name = f"coreir_lut{str(int(contents))}"
        self.io = IO(I=In(Bits[n]), O=Out(Bit))
        self.renamed_ports = coreir_port_mapping

        def _simulate(self, value_store, state_store):
            in_ = BitVector[n](value_store.get_value(getattr(self, "in")))
            value_store.set_value(self.out, contents.as_bool_list()[in_])
        self.simulate = _simulate
        self.coreir_name = "lutN"
        self.coreir_lib = "commonlib"
        self.coreir_genargs = {"N": n}
        self.coreir_configargs = {"init": contents}


def _to_int(value):
    if isinstance(value, Bit):
        if not value.const():
            raise ValueError(f"Unexpected Bit value: {value}")
        return 1 if value is Bit.VCC else 0
    if not isinstance(value, Bits):
        value = as_bits(value)
    return int(value)


class LUT(Generator2):
    """
    Generate a LUT containing entries of a generic Type
    """

    def __init__(self, T: Kind, n: int, contents: Tuple):
        """
        T: The type of each LUT entry (e.g. Bit or Bits[5])

        n: nubmer of entries in the LUT

        contents: the contents of the LUT (a tuple of length `n` containing
                  elements of type T that are constant)
        """
        num_bits_per_entry = T.flat_length()
        self.io = IO(I=In(Bits[clog2(n)]), O=Out(T))

        contents = tuple(BitVector[num_bits_per_entry](_to_int(c))
                         for c in contents)
        # create LUT for each bit in T
        luts = []
        for i in range(num_bits_per_entry):
            bv = BitVector[n]([elem[i] for elem in contents])
            luts.append(_CoreIRLUT(bv)())
        self.io.O @= from_bits(T, fork(luts)(as_bits(self.io.I)))
