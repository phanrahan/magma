from .compatibility import IntegerTypes
from .ref import AnonRef
from .bit import Bit, VCC, GND
from .array import ArrayType, ArrayKind
from .debug import debug_wire
import weakref

from hwtypes import BitVector, SIntVector

__all__ = ['Bits', 'BitsType', 'BitsKind']
__all__ += ['UInt', 'UIntType', 'UIntKind']
__all__ += ['SInt', 'SIntType', 'SIntKind']
__all__ += ['BFloat', 'BFloatKind']


class BitsKind(ArrayKind):
    _class_cache = weakref.WeakValueDictionary()

    def __str__(cls):
        if cls.isinput():
            return "In(Bits[{}])".format(cls.N)
        if cls.isoutput():
            return "Out(Bits[{}])".format(cls.N)
        return "Bits[{}]".format(cls.N)


    def __getitem__(cls, index):
        if isinstance(index, tuple):
            width, T = index
        else:
            width = index
            T = Bit
        if isinstance(width, Bits):
            assert width.const()
            # TODO: Move this logic to a method in BitsType
            bit_type_to_constant_map = {
                GND: 0,
                VCC: 1
            }
            width = BitVector[len(width)]([bit_type_to_constant_map[x] for x in
                                           width]).as_uint()
        try:
            result = BitsKind._class_cache[width, T]
            return result
        except KeyError:
            pass
        bases = [cls]
        bases = tuple(bases)
        class_name = '{}[{}, {}]'.format(cls.__name__, width, T.__name__)
        t = type(cls)(class_name, bases, dict(T=T, N=width))
        t.__module__ = cls.__module__
        BitsKind._class_cache[width, T] = t
        return t

    def qualify(cls, direction):
        if cls.T.isoriented(direction):
            return cls
        return Bits[cls.N, cls.T.qualify(direction)]

    def flip(cls):
        return Bits[cls.N, cls.T.flip()]

#     def __call__(cls, value=None, *args, **kwargs):
#         print(cls, cls.__dict__)
#         if value is not None:
#             if isinstance(value, (bool, IntegerTypes)):
#                 from .conversions import bits
#                 return bits(value, cls.N)
#             else:
#                 raise ValueError("Bit can only be initialized with None, bool, "
#                                  "or integer")
#         return super().__call__(*args, **kwargs)

    def get_family(self):
        import magma as m
        return m.get_family()


class Bits(ArrayType, metaclass=BitsKind):
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

    def zext(self, value):
        from .conversions import zext
        t = zext(self, value)
        return t

    def __getitem__(self, key):
        from .conversions import bits
        result = super().__getitem__(key)
        if isinstance(key, slice):
            return bits(result)
        return result


BitsType = Bits


# def Bits(N, T=None):
#     if T is None:
#         T = Bit
#     assert isinstance(N, (IntegerTypes, BitsType)), (N, type(N))
#     if isinstance(N, BitsType):
#         assert N.const()
#         # TODO: Move this logic to a method in BitsType
#         bit_type_to_constant_map = {
#             GND: 0,
#             VCC: 1
#         }
#         N = BitVector([bit_type_to_constant_map[x] for x in N]).as_uint()
#     name = 'Bits({})'.format(N)
#     return BitsKind(name, (BitsType,), dict(N=N, T=T))


class UIntKind(BitsKind):
    _class_cache = weakref.WeakValueDictionary()

    def __getitem__(cls, index):
        if isinstance(index, tuple):
            width, T = index
        else:
            width = index
            T = Bit
        if isinstance(width, UInt):
            assert width.const()
            # TODO: Move this logic to a method in BitsType
            bit_type_to_constant_map = {
                GND: 0,
                VCC: 1
            }
            width = BitVector[len(width)]([bit_type_to_constant_map[x] for x in
                                           width]).as_uint()
        try:
            return UIntKind._class_cache[width, T]
        except KeyError:
            pass
        bases = [cls]
        bases = tuple(bases)
        class_name = '{}[{}, {}]'.format(cls.__name__, width, T)
        t = type(cls)(class_name, bases, dict(T=T, N=width))
        t.__module__ = cls.__module__
        UIntKind._class_cache[width, T] = t
        return t

    def __str__(cls):
        if cls.isinput():
            return "In(UInt({}))".format(cls.N)
        if cls.isoutput():
            return "Out(UInt({}))".format(cls.N)
        return "UInt({})".format(cls.N)

    def qualify(cls, direction):
        if cls.T.isoriented(direction):
            return cls
        return UInt[cls.N, cls.T.qualify(direction)]

    def flip(cls):
        return UInt[cls.N, cls.T.flip()]


class UInt(Bits, metaclass=UIntKind):
    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        return 'uint([{}])'.format(', '.join(ts))

    def __getitem__(self, key):
        from .conversions import uint
        result = super().__getitem__(key)
        if isinstance(key, slice):
            return uint(result)
        return result


# def UInt(N, T=None):
#     if T is None:
#         T = Bit
#     assert isinstance(N, IntegerTypes)
#     name = 'UInt({})'.format(N)
#     return UIntKind(name, (UIntType,), dict(N=N, T=T))


class SIntKind(BitsKind):
    _class_cache = weakref.WeakValueDictionary()
    def __getitem__(cls, index):
        if isinstance(index, tuple):
            width, T = index
        else:
            width = index
            T = Bit
        if isinstance(width, SInt):
            assert width.const()
            # TODO: Move this logic to a method in BitsType
            bit_type_to_constant_map = {
                GND: 0,
                VCC: 1
            }
            width = BitVector[len(width)]([bit_type_to_constant_map[x] for x in
                                           width]).as_sint()
        try:
            return SIntKind._class_cache[width, T]
        except KeyError:
            pass
        bases = [cls]
        bases = tuple(bases)
        class_name = '{}[{}, {}]'.format(cls.__name__, width, T)
        t = type(cls)(class_name, bases, dict(T=T, N=width))
        t.__module__ = cls.__module__
        SIntKind._class_cache[width, T] = t
        return t

    def __str__(cls):
        if cls.isinput():
            return "In(SInt({}))".format(cls.N)
        if cls.isoutput():
            return "Out(SInt({}))".format(cls.N)
        return "SInt({})".format(cls.N)

    def qualify(cls, direction):
        if cls.T.isoriented(direction):
            return cls
        return SInt[cls.N, cls.T.qualify(direction)]

    def flip(cls):
        return SInt[cls.N, cls.T.flip()]


class SInt(Bits, metaclass=SIntKind):
    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        return 'sint([{}])'.format(', '.join(ts))

    def __int__(self):
        if not self.const():
            raise Exception("Can't call __int__ on a non-constant")
        return SIntVector(self.bits()).as_sint()

    def sext(self, value):
        from .conversions import sext
        return sext(self, value)

UIntType = UInt
SIntType = SInt


# def SInt(N, T=None):
#     if T is None:
#         T = Bit
#     assert isinstance(N, IntegerTypes)
#     name = 'SInt({})'.format(N)
#     return SIntKind(name, (SIntType,), dict(N=N, T=T))


class BFloatKind(BitsKind):
    _class_cache = weakref.WeakValueDictionary()

    def __getitem__(cls, index):
        if isinstance(index, tuple):
            width, T = index
        else:
            width = index
            T = Bit
        if isinstance(width, BFloat):
            assert width.const()
            # TODO: Move this logic to a method in BitsType
            bit_type_to_constant_map = {
                GND: 0,
                VCC: 1
            }
            width = BitVector[len(width)]([bit_type_to_constant_map[x] for x in
                                           width]).as_uint()
        try:
            return BFloatKind._class_cache[width, T]
        except KeyError:
            pass
        bases = [cls]
        bases = tuple(bases)
        class_name = '{}[{}, {}]'.format(cls.__name__, width, T)
        t = type(cls)(class_name, bases, dict(T=T, N=width))
        t.__module__ = cls.__module__
        BFloatKind._class_cache[width, T] = t
        return t

    def __str__(cls):
        if cls.isinput():
            return "In(BFloat({}))".format(cls.N)
        if cls.isoutput():
            return "Out(BFloat({}))".format(cls.N)
        return "BFloat({})".format(cls.N)

    def qualify(cls, direction):
        if cls.T.isoriented(direction):
            return cls
        return BFloat[cls.N, cls.T.qualify(direction)]

    def flip(cls):
        return BFloat[cls.N, cls.T.flip()]


class BFloat(Bits, metaclass=BFloatKind):
    def __repr__(self):
        if not isinstance(self.name, AnonRef):
            return repr(self.name)
        ts = [repr(t) for t in self.ts]
        return 'bfloat([{}])'.format(', '.join(ts))

    def __getitem__(self, key):
        from .conversions import bfloat
        result = super().__getitem__(key)
        if isinstance(key, slice):
            return bfloat(result)
        return result
