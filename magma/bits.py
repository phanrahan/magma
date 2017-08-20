from .compatibility import IntegerTypes
from .bit import Bit, BitOut, VCC, GND, BitType, BitKind
from .array import ArrayType, ArrayKind

__all__  = ['Bits', 'BitsType', 'BitsKind']
__all__ += ['UInt', 'UIntType', 'UIntKind']
__all__ += ['SInt', 'SIntType', 'SIntKind']

class BitsType(ArrayType):
    pass


class BitsKind(ArrayKind):
    def __str__(cls):
        return "Bits({})".format(cls.N)

    def qualify(cls, direction):
        if cls.T.isoriented(direction):
            return cls
        return Bits(cls.N, cls.T.qualify(direction))

    def flip(cls):
        return Bits(cls.N, cls.T.flip())


def Bits(N, T=None):
    if T is None:
        T = Bit
    assert isinstance(N, IntegerTypes)
    name = 'Bits({})'.format(N)
    return BitsKind(name, (BitsType,), dict(N=N, T=T))


class UIntType(BitsType):
    pass


class UIntKind(BitsKind):
    def __str__(cls):
        return "UInt({})".format(cls.N)

    def qualify(cls, direction):
        if cls.T.isoriented(direction):
            return cls
        return UInt(cls.N, cls.T.qualify(direction))

    def flip(cls):
        return UInt(cls.N, cls.T.flip())


def UInt(N, T=None):
    if T is None:
        T = Bit
    assert isinstance(N, IntegerTypes)
    name = 'UInt({})'.format(N)
    return UIntKind(name, (UIntType,), dict(N=N, T=T))


class SIntType(BitsType):
    pass


class SIntKind(BitsKind):
    def __str__(cls):
        return "SInt({})".format(cls.N)

    def qualify(cls, direction):
        if cls.T.isoriented(direction):
            return cls
        return SInt(cls.N, cls.T.qualify(direction))

    def flip(cls):
        return SInt(cls.N, cls.T.flip())


def SInt(N, T=None):
    if T is None:
        T = Bit
    assert isinstance(N, IntegerTypes)
    name = 'SInt({})'.format(N)
    return SIntKind(name, (SIntType,), dict(N=N, T=T))
