from magma.t import Type
from magma.bit import Bit, BitType, In, Out
from magma.array import Bits, BitsType, SInt, SIntType, UInt, UIntType
from magma.circuit import DeclareCircuit
from magma.compatibility import IntegerTypes
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


def type_check_binary_operator(operator):
    """
    For binary operations, the other argument must be the same type or a list
    of bits of the same length
    """
    def type_checked_operator(self, other):
        if not (isinstance(other, list) and len(self) == len(other)) and type(self) != type(other):
            raise TypeError("unsupported operand type(s) for {}: '{}' and"
                    "'{}'".format(operator.__name__, type(self), type(other)))
        return operator(self, other)
    return type_checked_operator


BitAnd = DeclareCircuit("And1", 'I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit))
BitOr = DeclareCircuit("Or1", 'I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit))
BitXor = DeclareCircuit("Xor1", 'I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit))
BitInvert = DeclareCircuit("Invert1", 'I', In(Bit), 'O', Out(Bit))

@type_check_binary_operator
def __and__(self, other):
    return BitAnd()(self, other)
BitType.__and__ = __and__

@type_check_binary_operator
def __or__(self, other):
    return BitOr()(self, other)
BitType.__or__ = __or__

@type_check_binary_operator
def __xor__(self, other):
    return BitXor()(self, other)
BitType.__xor__ = __xor__

def __invert__(self):
    return BitInvert()(self)
BitType.__invert__ = __invert__


@lru_cache(maxsize=None)
def DeclareAndN(N):
    T = Bits(N)
    return DeclareCircuit("And{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))


@type_check_binary_operator
def __and__(self, other):
    return DeclareAndN(self.N)()(self, other)
BitsType.__and__ = __and__


@lru_cache(maxsize=None)
def DeclareOrN(N):
    T = Bits(N)
    return DeclareCircuit("Or{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))


@type_check_binary_operator
def __or__(self, other):
    return DeclareOrN(self.N)()(self, other)
BitsType.__or__ = __or__


@lru_cache(maxsize=None)
def DeclareXorN(N):
    T = Bits(N)
    return DeclareCircuit("Xor{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))

@type_check_binary_operator
def __xor__(self, other):
    return DeclareXorN(self.N)()(self, other)
BitsType.__xor__ = __xor__


@lru_cache(maxsize=None)
def DeclareInvertN(N):
    T = Bits(N)
    return DeclareCircuit("Invert{}".format(N), 'I', In(T), 'O', Out(T))

def __invert__(self):
    return DeclareInvertN(self.N)()(self)
BitsType.__invert__ = __invert__


@lru_cache(maxsize=None)
def DeclareShiftLeftN(N, amount):
    T = Bits(N)
    return DeclareCircuit("ShiftLeft{}_{}".format(N, amount), 'I', In(T), 'O', Out(T))


@lru_cache(maxsize=None)
def DeclareDynamicShiftLeftN(N):
    T = Bits(N)
    i1_type = Bits((N - 1).bit_length())
    return DeclareCircuit("DynamicShiftLeft{}".format(N), 'I0', In(T), 'I1', In(i1_type), 'O', Out(T))

def __lshift__(self, other):
    if isinstance(other, IntegerTypes):
        return DeclareShiftLeftN(self.N, other)()(self)
    elif isinstance(other, Type):
        return DeclareDynamicShiftLeftN(self.N)()(self, other)
    else:
        raise TypeError("<< not implemented for argument 2 of type {}".format(type(other)))
BitsType.__lshift__ = __lshift__


@lru_cache(maxsize=None)
def DeclareShiftRightN(N, amount):
    T = Bits(N)
    return DeclareCircuit("ShiftRight{}_{}".format(N, amount), 'I', In(T), 'O', Out(T))


@lru_cache(maxsize=None)
def DeclareDynamicShiftRightN(N):
    T = Bits(N)
    i1_type = Bits((N - 1).bit_length())
    return DeclareCircuit("DynamicShiftRight{}".format(N), 'I0', In(T), 'I1', In(i1_type), 'O', Out(T))

def __rshift__(self, other):
    if isinstance(other, IntegerTypes):
        return DeclareShiftRightN(self.N, other)()(self)
    elif isinstance(other, Type):
        return DeclareDynamicShiftRightN(self.N)()(self, other)
    else:
        raise TypeError(">> not implemented for argument 2 of type {}".format(type(other)))
BitsType.__rshift__ = __rshift__


@lru_cache(maxsize=None)
def DeclareSignedAddN(N):
    T = SInt(N)
    return DeclareCircuit("SignedAdd{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))

@type_check_binary_operator
def __add__(self, other):
    return DeclareSignedAddN(self.N)()(self, other)
SIntType.__add__ = __add__


@lru_cache(maxsize=None)
def DeclareSignedSubN(N):
    T = SInt(N)
    return DeclareCircuit("SignedSub{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))

@type_check_binary_operator
def __sub__(self, other):
    return DeclareSignedSubN(self.N)()(self, other)
SIntType.__sub__ = __sub__


@lru_cache(maxsize=None)
def DeclareSignedMulN(N):
    T = SInt(N)
    return DeclareCircuit("SignedMul{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))

@type_check_binary_operator
def __mul__(self, other):
    return DeclareSignedMulN(self.N)()(self, other)
SIntType.__mul__ = __mul__


@lru_cache(maxsize=None)
def DeclareSignedDivN(N):
    T = SInt(N)
    return DeclareCircuit("SignedDiv{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))

@type_check_binary_operator
def __truediv__(self, other):
    return DeclareSignedDivN(self.N)()(self, other)
SIntType.__truediv__ = __truediv__
SIntType.__div__ = __truediv__


@lru_cache(maxsize=None)
def DeclareSignedLtN(N):
    T = SInt(N)
    return DeclareCircuit("SignedLt{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(Bit))

@type_check_binary_operator
def __lt__(self, other):
    return DeclareSignedLtN(self.N)()(self, other)
SIntType.__lt__ = __lt__


@lru_cache(maxsize=None)
def DeclareSignedLtEN(N):
    T = SInt(N)
    return DeclareCircuit("SignedLtE{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(Bit))

@type_check_binary_operator
def __le__(self, other):
    return DeclareSignedLtEN(self.N)()(self, other)
SIntType.__le__ = __le__


@lru_cache(maxsize=None)
def DeclareSignedGtN(N):
    T = SInt(N)
    return DeclareCircuit("SignedGt{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(Bit))

@type_check_binary_operator
def __gt__(self, other):
    return DeclareSignedGtN(self.N)()(self, other)
SIntType.__gt__ = __gt__


@lru_cache(maxsize=None)
def DeclareSignedGtEN(N):
    T = SInt(N)
    return DeclareCircuit("SignedGtE{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(Bit))

@type_check_binary_operator
def __gte__(self, other):
    return DeclareSignedGtEN(self.N)()(self, other)
SIntType.__gte__ = __gte__


@lru_cache(maxsize=None)
def DeclareUnsignedAddN(N):
    T = UInt(N)
    return DeclareCircuit("UnsignedAdd{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))

@type_check_binary_operator
def __add__(self, other):
    return DeclareUnsignedAddN(self.N)()(self, other)
UIntType.__add__ = __add__


@lru_cache(maxsize=None)
def DeclareUnsignedSubN(N):
    T = UInt(N)
    return DeclareCircuit("UnsignedSub{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))

@type_check_binary_operator
def __sub__(self, other):
    return DeclareUnsignedSubN(self.N)()(self, other)
UIntType.__sub__ = __sub__


@lru_cache(maxsize=None)
def DeclareUnsignedMulN(N):
    T = UInt(N)
    return DeclareCircuit("UnsignedMul{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))

@type_check_binary_operator
def __mul__(self, other):
    return DeclareUnsignedMulN(self.N)()(self, other)
UIntType.__mul__ = __mul__


@lru_cache(maxsize=None)
def DeclareUnsignedDivN(N):
    T = UInt(N)
    return DeclareCircuit("UnsignedDiv{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))

@type_check_binary_operator
def __truediv__(self, other):
    return DeclareUnsignedDivN(self.N)()(self, other)
UIntType.__truediv__ = __truediv__
UIntType.__div__ = __truediv__


@lru_cache(maxsize=None)
def DeclareUnsignedLtN(N):
    T = UInt(N)
    return DeclareCircuit("UnsignedLt{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(Bit))

@type_check_binary_operator
def __lt__(self, other):
    return DeclareUnsignedLtN(self.N)()(self, other)
UIntType.__lt__ = __lt__


@lru_cache(maxsize=None)
def DeclareUnsignedLtEN(N):
    T = UInt(N)
    return DeclareCircuit("UnsignedLtE{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(Bit))

@type_check_binary_operator
def __le__(self, other):
    return DeclareUnsignedLtEN(self.N)()(self, other)
UIntType.__le__ = __le__


@lru_cache(maxsize=None)
def DeclareUnsignedGtN(N):
    T = UInt(N)
    return DeclareCircuit("UnsignedGt{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(Bit))

@type_check_binary_operator
def __gt__(self, other):
    return DeclareUnsignedGtN(self.N)()(self, other)
UIntType.__gt__ = __gt__


@lru_cache(maxsize=None)
def DeclareUnsignedGtEN(N):
    T = UInt(N)
    return DeclareCircuit("UnsignedGtE{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(Bit))

@type_check_binary_operator
def __gte__(self, other):
    return DeclareUnsignedGtEN(self.N)()(self, other)
UIntType.__gte__ = __gte__
