from __future__ import division

from .compatibility import IntegerTypes, StringTypes
from .bitutils import seq2int, int2seq
import numpy as np


class BitVector:
    def __init__(self, value=0, num_bits=None, signed=False):
        self.signed = signed
        if isinstance(value, IntegerTypes):
            if num_bits is None:
                num_bits = max(value.bit_length(), 1)
            self._value = value
            self._bits = int2seq(value, num_bits)
        elif isinstance(value, list):
            if not (all(x == 0 or x == 1 for x in value) or all(x == False or x == True for x in value)):
                raise Exception("BitVector list initialization must be a list of 0s and 1s or a list of True and False")
            if num_bits is None:
                num_bits = len(value)
            self._value = seq2int(value)
            self._bits = value
            if self.signed and self._bits[-1]:
                self._value -= (1 << num_bits)
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
            if other < 0:
                raise ValueError("Cannot shift by negative value {}".format(other))
            shift_result = self._value << other
        else:
            assert isinstance(other, BitVector)
            if other.as_int() < 0:
                raise ValueError("Cannot shift by negative value {}".format(other))
            shift_result = self._value << other._value
        mask = (1 << self.num_bits) - 1
        return BitVector(shift_result & mask, num_bits=self.num_bits)

    def __rshift__(self, other):
        """
        numpy.right_shift is a logical right shift, Python defaults to arithmetic
        .item() returns a python type
        """
        if isinstance(other, int):
            if other < 0:
                raise ValueError("Cannot shift by negative value {}".format(other))
            shift_result = np.right_shift(self._value,  other).item()
        else:
            assert isinstance(other, BitVector)
            if other.as_int() < 0:
                raise ValueError("Cannot shift by negative value {}".format(other))
            shift_result = np.right_shift(self._value,  other._value).item()
        mask = (1 << self.num_bits) - 1
        return BitVector(shift_result & mask, num_bits=self.num_bits)

    def arithmetic_shift_right(self, other):
        if isinstance(other, int):
            if other < 0:
                raise ValueError("Cannot shift by negative value {}".format(other))
            shift_result = self._value >> other
        else:
            assert isinstance(other, BitVector)
            if other.as_int() < 0:
                raise ValueError("Cannot shift by negative value {}".format(other))
            shift_result = self._value >> other._value
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
        result = self._value // other._value
        mask = (1 << self.num_bits) - 1
        return BitVector(result & mask, num_bits=self.num_bits)

    def __truediv__(self, other):
        assert isinstance(other, BitVector)
        result = self._value // other._value
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

    def as_binary_string(self):
        return "0b" + np.binary_repr(self.as_int(), self.num_bits)

    def as_bool_list(self):
        return [bool(x) for x in self._bits]

    def __len__(self):
        return self.num_bits

    def __str__(self):
        return str(self._value)

    def __invert__(self):
        retval = ~self._value
        if not self.signed:
            retval = retval & (1 << self.num_bits) - 1
        return BitVector(retval, num_bits=self.num_bits)

    def __eq__(self, other):
        if isinstance(other, BitVector):
            return BitVector(self._value == other._value, num_bits=1)
        elif isinstance(other, list) and all(isinstance(x, bool) for x in other):
            return self.as_bool_list() == other
        elif isinstance(other, bool) and self.num_bits == 1:
            return self.as_bool_list()[0] == other
        raise NotImplementedError()
