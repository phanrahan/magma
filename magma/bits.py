from .compatibility import IntegerTypes
from .ref import AnonRef
from .bit import Bit, VCC, GND
from .array import ArrayType, ArrayKind
from .debug import debug_wire

from bit_vector import BitVector, SIntVector

__all__ = ['Bits', 'BitsType', 'BitsKind']
__all__ += ['UInt', 'UIntType', 'UIntKind']
__all__ += ['SInt', 'SIntType', 'SIntKind']


class BitsType(ArrayType):
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
        return BitVector(self.bits()).as_int()

    @debug_wire
    def wire(i, o, debug_info):
        if isinstance(o, IntegerTypes):
            if o.bit_length() > len(i):
                raise ValueError(
                    f"Cannot convert integer {o} (bit_length={o.bit_length()}) to Bits({len(i)})")
            from .conversions import bits
            o = bits(o, len(i))
        super().wire(o, debug_info)


class BitsKind(ArrayKind):
    def __str__(cls):
        if cls.isinput():
            return "In(Bits({}))".format(cls.N)
        if cls.isoutput():
            return "Out(Bits({}))".format(cls.N)
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
    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        return 'uint([{}])'.format(', '.join(ts))


class UIntKind(BitsKind):
    def __str__(cls):
        if cls.isinput():
            return "In(UInt({}))".format(cls.N)
        if cls.isoutput():
            return "Out(UInt({}))".format(cls.N)
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
    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        return 'sint([{}])'.format(', '.join(ts))

    def __int__(self):
        if not self.const():
            raise Exception("Can't call __int__ on a non-constant")
        return SIntVector(self.bits()).as_sint()


class SIntKind(BitsKind):
    def __str__(cls):
        if cls.isinput():
            return "In(SInt({}))".format(cls.N)
        if cls.isoutput():
            return "Out(SInt({}))".format(cls.N)
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
