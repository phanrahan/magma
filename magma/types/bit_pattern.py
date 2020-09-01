"""
Based on chisel BitPat
https://github.com/freechipsproject/chisel3/blob/v3.3.2/src/main/scala/chisel3/util/BitPat.scala
"""
import string

from hwtypes import BitVector

from magma.bits import Bits


class BitPattern:
    def __init__(self, pattern):
        """
        Parses a bit pattern string `pattern` into the attributes `bits`,
        `mask`, `width`

        * `bits`  - the literal value, with don't cares being 0
        * `mask`  - the mask bits, with don't cares being 0 and cares being 1
        * `width` - the number of bits in the literal, including values and
                    don't cares, but not including the white space and
                    underscores
        """
        if pattern[0] != "b":
            raise ValueError("BitPattern must be in binary and prefixed with "
                             "'b'")
        bits = 0
        mask = 0
        count = 0
        for digit in pattern[1:]:
            if digit == '_' or digit in string.whitespace:
                continue
            if digit not in "01?":
                raise ValueError(
                    f"BitPattern {pattern} contains illegal character: {d}"
                )
            mask = (mask << 1) + (0 if digit == "?" else 1)
            bits = (bits << 1) + (1 if digit == "1" else 0)
            count += 1
        self.bits = BitVector[count](bits)
        self.mask = BitVector[count](mask)
        self.width = count
        self.const = self.mask == ((1 << self.width) - 1)
        self.__hash = hash(pattern)

    def __eq__(self, other):
        if not isinstance(other, Bits):
            raise TypeError(
                "BitPattern can only be compared to Bits"
            )
        return self.bits == (other & self.mask)

    def as_bv(self):
        if not self.const:
            raise TypeError(
                "Can only convert BitPattern with no don't cares to int"
            )
        return self.bits

    def __hash__(self):
        return self.__hash
