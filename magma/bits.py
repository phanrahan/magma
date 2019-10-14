"""
Defines a subtype of m.Array called m.Bits

m.Bits[N] is roughly equivalent ot m.Array[N, T]
"""
import weakref
import typing as tp
from hwtypes import BitVector, SIntVector
from hwtypes import AbstractBitVector, AbstractBitVectorMeta, AbstractBit

import magma as m
from .compatibility import IntegerTypes
from .ref import AnonRef
from .bit import Bit, VCC, GND
from .array import Array, ArrayMeta
from .debug import debug_wire


# __all__ = ['Bits', 'BitsType', 'BitsKind']
# __all__ += ['UInt', 'UIntType', 'UIntKind']
# __all__ += ['SInt', 'SIntType', 'SIntKind']
# __all__ += ['BFloat', 'BFloatKind']


class BitsMeta(AbstractBitVectorMeta, ArrayMeta):
    def __new__(mcs, name, bases, namespace, info=(None, None, None), **kwargs):
        return ArrayMeta.__new__(mcs, name, bases, namespace, info, **kwargs)

    def __getitem__(cls, index):
        if isinstance(index, int):
            index = (index, Bit)
        return ArrayMeta.__getitem__(cls, index)

    def __str__(cls):
        name = f"{cls.orig_name}[{cls.N}]"
        if cls.is_input():
            name = f"In({name})"
        elif cls.is_output():
            name = f"Out({name})"
        elif cls.is_output():
            name = f"InOut({name})"
        return name


class Bits(Array, AbstractBitVector, metaclass=BitsMeta):
    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        return 'bits([{}])'.format(', '.join(ts))

    def bits(self):
        if not self.const():
            raise Exception("Not a constant")

        def convert(x):
            if x is VCC:
                return True
            assert x is GND
            return False
        return [convert(x) for x in self.ts]

    def __int__(self):
        if not self.const():
            raise Exception("Can't call __int__ on a non-constant")
        return BitVector[len(self)](self.bits()).as_int()

    @debug_wire
    def wire(i, o, debug_info):
        if isinstance(o, IntegerTypes):
            if o.bit_length() > len(i):
                raise ValueError(
                    f"Cannot convert integer {o} (bit_length={o.bit_length()}) to Bits({len(i)})")
            from .conversions import bits
            o = bits(o, len(i))
        super().wire(o, debug_info)

    def zext(self, value):
        from .conversions import zext
        t = zext(self, value)
        return t

    def __getitem__(self, key):
        result = super().__getitem__(key)
        if isinstance(key, slice):
            return Bits[len(result)](result)
        return result

    @classmethod
    def make_constant(self, value, num_bits:tp.Optional[int]=None) -> 'AbstractBitVector':
        raise NotImplementedError()

    def __setitem__(self, index : int, value : AbstractBit):
        raise NotImplementedError()

    def bvnot(self) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvand(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvnand(self, other) -> 'AbstractBitVector':
        return self.bvand(other).bvnot()

    def bvor(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvnor(self, other) -> 'AbstractBitVector':
        return self.bvor(other).bvnot()

    def bvxor(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvxnor(self, other) -> 'AbstractBitVector':
        return self.bvxor(other).bvnot()

    def bvshl(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvlshr(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvashr(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvrol(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvror(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvcomp(self, other) -> 'AbstractBitVector[1]':
        raise NotImplementedError()

    def bveq(self, other) -> AbstractBit:
        raise NotImplementedError()

    def bvne(self, other) -> AbstractBit:
        return ~self.bveq(other)

    def bvult(self, other) -> AbstractBit:
        raise NotImplementedError()

    def bvule(self, other) -> AbstractBit:
        return self.bvult(other) | self.bveq(other)

    def bvugt(self, other) -> AbstractBit:
        return ~self.bvule(other)

    def bvuge(self, other) -> AbstractBit:
        return ~self.bvult(other)

    def bvslt(self, other) -> AbstractBit:
        raise NotImplementedError()

    def bvsle(self, other) -> AbstractBit:
        return self.bvslt(other) | self.bveq(other)

    def bvsgt(self, other) -> AbstractBit:
        return ~self.bvsle(other)

    def bvsge(self, other) -> AbstractBit:
        return ~self.bvslt(other)

    def bvneg(self) -> 'AbstractBitVector':
        raise NotImplementedError()

    def adc(self, other, carry) -> tp.Tuple['AbstractBitVector', AbstractBit]:
        raise NotImplementedError()

    def ite(i,t,e) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvadd(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvsub(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvmul(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvudiv(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvurem(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvsdiv(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def bvsrem(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def repeat(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def sext(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def ext(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()

    def zext(self, other) -> 'AbstractBitVector':
        raise NotImplementedError()


BitsType = Bits


# class UInt(Bits):
#     def __repr__(self):
#         if not isinstance(self.name, AnonRef):
#             return repr(self.name)
#         ts = [repr(t) for t in self.ts]
#         return 'uint([{}])'.format(', '.join(ts))

#     def __getitem__(self, key):
#         from .conversions import uint
#         result = super().__getitem__(key)
#         if isinstance(key, slice):
#             return uint(result)
#         return result


# class SInt(Bits):
#     def __repr__(self):
#         if not isinstance(self.name, AnonRef):
#             return repr(self.name)
#         ts = [repr(t) for t in self.ts]
#         return 'sint([{}])'.format(', '.join(ts))

#     def __int__(self):
#         if not self.const():
#             raise Exception("Can't call __int__ on a non-constant")
#         return SIntVector[len(self)](self.bits()).as_sint()

#     def sext(self, value):
#         from .conversions import sext
#         return sext(self, value)

# UIntType = UInt
# SIntType = SInt


class BFloat(Bits):
    pass
    # def __getitem__(self, key):
    #     result = super().__getitem__(key)
    #     if isinstance(key, slice):
    #         return BFloat[len(result)](result)
    #     return result
