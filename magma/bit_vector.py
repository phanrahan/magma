from magma.compatibility import IntegerTypes, StringTypes
from magma.bits import seq2int, int2seq

class BitVector:
    def __init__(self, value=0, num_bits=None):
        if isinstance(value, IntegerTypes):
            if num_bits is None:
                num_bits = max(value.bit_length(), 1)
            self._value = value
            self._bits = int2seq(value)
        elif isinstance(value, list):
            if not all(x == 0 or x == 1 for x in value):
                raise Exception("BitVector list initialization must be a list of 0s and 1s")
            if num_bits is None:
                num_bits = len(value)
            self._value = seq2int(value)
            self._bits = value
        else:
            raise Exception("BitVector initialization with type {} not supported".format(type(value)))
        self.num_bits = num_bits

    def __and__(self, other):
        assert isinstance(other, BitVector)
        return BitVector(self._value & other._value, num_bits=self.num_bits)

    def __or__(self, other):
        assert isinstance(other, BitVector)
        return BitVector(self._value | other._value, num_bits=self.num_bits)

    def __xor__(self, other):
        assert isinstance(other, BitVector)
        return BitVector(self._value ^ other._value, num_bits=self.num_bits)

    def as_int(self):
        return self._value
