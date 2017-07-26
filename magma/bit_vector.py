from magma.compatibility import IntegerTypes, StringTypes
from magma.bits import seq2int, int2seq
import numpy as np

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

    def __lshift__(self, other):
        if isinstance(other, int):
            shift_result = self._value << other
        else:
            assert isinstance(other, BitVector)
            shift_result = self._value << other._value
        mask = (1 << self.num_bits) - 1
        return BitVector(shift_result & mask, num_bits=self.num_bits)

    def __rshift__(self, other):
        """
        numpy.right_shift is a logical right shift, Python defaults to arithmetic
        .item() returns a python type
        """
        if isinstance(other, int):
            shift_result = np.right_shift(self._value,  other).item()
        else:
            assert isinstance(other, BitVector)
            shift_result = np.right_shift(self._value,  other._value).item()
        mask = (1 << self.num_bits) - 1
        return BitVector(shift_result & mask, num_bits=self.num_bits)

    def __add__(self, other):
        assert isinstance(other, BitVector)
        result = self._value + other._value
        mask = (1 << self.num_bits) - 1
        return BitVector(result & mask, num_bits=self.num_bits)

    def __sub__(self, other):
        assert isinstance(other, BitVector)
        result = self._value - other._value
        mask = (1 << self.num_bits) - 1
        return BitVector(result & mask, num_bits=self.num_bits)

    def __mul__(self, other):
        assert isinstance(other, BitVector)
        result = self._value * other._value
        mask = (1 << self.num_bits) - 1
        return BitVector(result & mask, num_bits=self.num_bits)

    def __div__(self, other):
        assert isinstance(other, BitVector)
        result = self._value / other._value
        mask = (1 << self.num_bits) - 1
        return BitVector(result & mask, num_bits=self.num_bits)

    def __lt__(self, other):
        assert isinstance(other, BitVector)
        return BitVector(int(self._value < other._value), num_bits=1)

    def __le__(self, other):
        assert isinstance(other, BitVector)
        return BitVector(int(self._value <= other._value), num_bits=1)

    def __gt__(self, other):
        assert isinstance(other, BitVector)
        return BitVector(int(self._value > other._value), num_bits=1)

    def __ge__(self, other):
        assert isinstance(other, BitVector)
        return BitVector(int(self._value >= other._value), num_bits=1)

    def as_int(self):
        return self._value
