from magma.compatibility import IntegerTypes, StringTypes
from magma.bits import seq2int, int2seq

class BitVector:
    def __init__(self, value=0):
        if isinstance(value, IntegerTypes):
            self._num_bits = max(value.bit_length(), 1)
            self._value = value
            self._bits = int2seq(value)
        elif isinstance(value, list):
            if not all(x == 0 or x == 1 for x in value):
                raise Exception("BitVector list initialization must be a list of 0s and 1s")
            self.num_bits = len(value)
            self._value = seq2int(value)
            self._bits = value
        else:
            raise Exception("BitVector initialization with type {} not supported".format(type(value)))

    def __and__(self, other):
        assert isinstance(other, BitVector)
        return BitVector(self._value & other._value)

    def __or__(self, other):
        assert isinstance(other, BitVector)
        return BitVector(self._value | other._value)

    def __xor__(self, other):
        assert isinstance(other, BitVector)
        return BitVector(self._value ^ other._value)

    def as_int(self):
        return self._value
