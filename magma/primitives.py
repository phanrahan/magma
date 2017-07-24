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
        if not (isinstance(other, list) and len(self) == len(other)) and \
           type(self) != type(other):
            raise TypeError("unsupported operand type(s) for {}: '{}' and"
                            "'{}'".format(operator.__name__, type(self),
                                          type(other)))
        return operator(self, other)
    return type_checked_operator


def declare_bit_binop(name, op):
    circ = DeclareCircuit("{}1".format(name), 
                          'I0', In(Bit), 'I1', In(Bit), 'O', Out(Bit))

    @type_check_binary_operator
    def func(self, other):
        return circ()(self, other)
    func.__name__ = op
    setattr(BitType, op, func)


declare_bit_binop("And", "__and__")
declare_bit_binop("Or", "__or__")
declare_bit_binop("Xor", "__xor__")

BitInvert = DeclareCircuit("Invert1", 'I', In(Bit), 'O', Out(Bit))


def __invert__(self):
    return BitInvert()(self)


BitType.__invert__ = __invert__


def declare_bits_binop(name, op):
    @lru_cache(maxsize=None)
    def Declare(N):
        T = Bits(N)
        return DeclareCircuit("{}{}".format(name, N),
                              'I0', In(T), 'I1', In(T), 'O', Out(T))

    @type_check_binary_operator
    def func(self, other):
        return Declare(self.N)()(self, other)
    func.__name__ = op
    setattr(BitsType, op, func)


declare_bits_binop("And", "__and__")
declare_bits_binop("Or", "__or__")
declare_bits_binop("Xor", "__xor__")


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
    return DeclareCircuit("ShiftLeft{}_{}".format(N, amount),
                          'I', In(T), 'O', Out(T))


@lru_cache(maxsize=None)
def DeclareDynamicShiftLeftN(N):
    T = Bits(N)
    i1_type = Bits((N - 1).bit_length())
    return DeclareCircuit("DynamicShiftLeft{}".format(N),
                          'I0', In(T), 'I1', In(i1_type), 'O', Out(T))


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
    return DeclareCircuit("ShiftRight{}_{}".format(N, amount),
                          'I', In(T), 'O', Out(T))


@lru_cache(maxsize=None)
def DeclareDynamicShiftRightN(N):
    T = Bits(N)
    i1_type = Bits((N - 1).bit_length())
    return DeclareCircuit("DynamicShiftRight{}".format(N),
                          'I0', In(T), 'I1', In(i1_type), 'O', Out(T))


def __rshift__(self, other):
    if isinstance(other, IntegerTypes):
        return DeclareShiftRightN(self.N, other)()(self)
    elif isinstance(other, Type):
        return DeclareDynamicShiftRightN(self.N)()(self, other)
    else:
        raise TypeError(">> not implemented for argument 2 of type {}".format(
            type(other)))


BitsType.__rshift__ = __rshift__


def declare_binop(name, _type, type_type, op, out_type=None):
    @lru_cache(maxsize=None)
    def Declare(N):
        T = _type(N)
        return DeclareCircuit("{}{}".format(name, N),
                              'I0', In(T), 'I1', In(T),
                              'O', Out(out_type if out_type else T))

    @type_check_binary_operator
    def func(self, other):
        return Declare(self.N)()(self, other)
    func.__name__ = op
    setattr(type_type, op, func)


declare_binop("SignedAdd", SInt, SIntType, "__add__")
declare_binop("SignedSub", SInt, SIntType, "__sub__")
declare_binop("SignedMul", SInt, SIntType, "__mul__")
declare_binop("SignedDiv", SInt, SIntType, "__div__")
declare_binop("SignedDiv", SInt, SIntType, "__truediv__")
declare_binop("SignedLt",  SInt, SIntType, "__lt__", out_type=Bit)
declare_binop("SignedLtE", SInt, SIntType, "__le__", out_type=Bit)
declare_binop("SignedGt",  SInt, SIntType, "__gt__", out_type=Bit)
declare_binop("SignedGtE", SInt, SIntType, "__ge__", out_type=Bit)

declare_binop("UnsignedAdd", UInt, UIntType, "__add__")
declare_binop("UnsignedSub", UInt, UIntType, "__sub__")
declare_binop("UnsignedMul", UInt, UIntType, "__mul__")
declare_binop("UnsignedDiv", UInt, UIntType, "__div__")
declare_binop("UnsignedDiv", UInt, UIntType, "__truediv__")
declare_binop("UnsignedLt",  UInt, UIntType, "__lt__", out_type=Bit)
declare_binop("UnsignedLtE", UInt, UIntType, "__le__", out_type=Bit)
declare_binop("UnsignedGt",  UInt, UIntType, "__gt__", out_type=Bit)
declare_binop("UnsignedGtE", UInt, UIntType, "__ge__", out_type=Bit)
