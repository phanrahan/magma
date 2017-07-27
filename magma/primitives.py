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
    circ = DeclareCircuit("{}".format(name),
                          'in0', In(Bit), 'in1', In(Bit), 'out', Out(Bit))

    @type_check_binary_operator
    def func(self, other):
        return circ(WIDTH=1)(self, other)
    func.__name__ = op
    setattr(BitType, op, func)


declare_bit_binop("coreir_and", "__and__")
declare_bit_binop("coreir_or", "__or__")
declare_bit_binop("coreir_xor", "__xor__")

BitInvert = DeclareCircuit("coreir_not", 'in', In(Bit), 'out', Out(Bit))


def __invert__(self):
    return BitInvert(WIDTH=1)(self)


BitType.__invert__ = __invert__


def declare_bits_binop(name, op):
    @lru_cache(maxsize=None)
    def Declare(N):
        T = Bits(N)
        return DeclareCircuit("{}".format(name),
                              'in0', In(T), 'in1', In(T), 'out', Out(T))

    @type_check_binary_operator
    def func(self, other):
        return Declare(self.N)(WIDTH=self.N)(self, other)
    func.__name__ = op
    setattr(BitsType, op, func)


declare_bits_binop("coreir_and", "__and__")
declare_bits_binop("coreir_or", "__or__")
declare_bits_binop("coreir_xor", "__xor__")


@lru_cache(maxsize=None)
def DeclareInvertN(N):
    T = Bits(N)
    return DeclareCircuit("coreir_not", 'in', In(T), 'out', Out(T))


def __invert__(self):
    return DeclareInvertN(self.N)(WIDTH=self.N)(self)


BitsType.__invert__ = __invert__


@lru_cache(maxsize=None)
def DeclareShiftLeft(N):
    T = Bits(N)
    return DeclareCircuit("coreir_shl", 'in', In(UInt(N)), 'out', Out(T))


@lru_cache(maxsize=None)
def DeclareDynamicShiftLeft(N):
    T = Bits(N)
    # i1_type = Bits((N - 1).bit_length())
    return DeclareCircuit("coreir_dshl",
                          'in0', In(T), 'in1', In(UInt(N)), 'out', Out(T))


def __lshift__(self, other):
    if isinstance(other, IntegerTypes):
        if other < 0:
            raise ValueError("Second argument to << must be positive, not {}".format(other))
        return DeclareShiftLeft(self.N)(WIDTH=self.N, SHIFTBITS=other)(self)
    elif isinstance(other, Type):
        if not isinstance(other, UIntType):
            raise TypeError("Second argument to << must be a UInt, not {}".format(type(other)))
        return DeclareDynamicShiftLeft(self.N)(WIDTH=self.N)(self, other)
    else:
        raise TypeError("<< not implemented for argument 2 of type {}".format(
            type(other)))


BitsType.__lshift__ = __lshift__


@lru_cache(maxsize=None)
def DeclareShiftRight(N):
    T = Bits(N)
    return DeclareCircuit("coreir_lshr", 'in', In(UInt(N)), 'out', Out(T))


@lru_cache(maxsize=None)
def DeclareDynamicShiftRight(N):
    T = Bits(N)
    # i1_type = Bits((N - 1).bit_length())
    return DeclareCircuit("coreir_dlshr",
                          'in0', In(T), 'in1', In(UInt(N)), 'out', Out(T))


def __rshift__(self, other):
    if isinstance(other, IntegerTypes):
        if other < 0:
            raise ValueError("Second argument to >> must be positive, not {}".format(other))
        return DeclareShiftRight(self.N)(WIDTH=self.N, SHIFTBITS=other)(self)
    elif isinstance(other, Type):
        if not isinstance(other, UIntType):
            raise TypeError("Second argument to >> must be a UInt, not {}".format(type(other)))
        return DeclareDynamicShiftRight(self.N)(WIDTH=self.N)(self, other)
    else:
        raise TypeError(">> not implemented for argument 2 of type {}".format(
            type(other)))


BitsType.__rshift__ = __rshift__


def declare_binop(name, _type, type_type, op, out_type=None):
    @lru_cache(maxsize=None)
    def Declare(N):
        T = _type(N)
        return DeclareCircuit("{}".format(name),
                              'in0', In(T), 'in1', In(T),
                              'out', Out(out_type if out_type else T))

    @type_check_binary_operator
    def func(self, other):
        return Declare(self.N)(WIDTH=self.N)(self, other)
    func.__name__ = op
    setattr(type_type, op, func)


declare_binop("coreir_add", SInt, SIntType, "__add__")
declare_binop("coreir_sub", SInt, SIntType, "__sub__")
declare_binop("coreir_mul", SInt, SIntType, "__mul__")
declare_binop("coreir_sdiv", SInt, SIntType, "__div__")
declare_binop("coreir_sdiv", SInt, SIntType, "__truediv__")
declare_binop("coreir_slt",  SInt, SIntType, "__lt__", out_type=Bit)
declare_binop("coreir_sle", SInt, SIntType, "__le__", out_type=Bit)
declare_binop("coreir_sgt",  SInt, SIntType, "__gt__", out_type=Bit)
declare_binop("coreir_sge", SInt, SIntType, "__ge__", out_type=Bit)

declare_binop("coreir_add", UInt, UIntType, "__add__")
declare_binop("coreir_sub", UInt, UIntType, "__sub__")
declare_binop("coreir_mul", UInt, UIntType, "__mul__")
declare_binop("coreir_udiv", UInt, UIntType, "__div__")
declare_binop("coreir_udiv", UInt, UIntType, "__truediv__")
declare_binop("coreir_ult",  UInt, UIntType, "__lt__", out_type=Bit)
declare_binop("coreir_ule", UInt, UIntType, "__le__", out_type=Bit)
declare_binop("coreir_ugt",  UInt, UIntType, "__gt__", out_type=Bit)
declare_binop("coreir_uge", UInt, UIntType, "__ge__", out_type=Bit)


@lru_cache(maxsize=None)
def DeclareArithmeticShiftRight(N):
    T = SInt(N)
    return DeclareCircuit("coreir_ashr", 'in', In(UInt(N)), 'out', Out(T))


@lru_cache(maxsize=None)
def DeclareDynamicArithmeticShiftRight(N):
    T = SInt(N)
    # i1_type = Bits((N - 1).bit_length())
    return DeclareCircuit("coreir_dashr",
                          'in0', In(T), 'in1', In(UInt(N)), 'out', Out(T))


def arithmetic_shift_right(self, other):
    if isinstance(other, IntegerTypes):
        if other < 0:
            raise ValueError("Second argument to arithmetic_shift_right must be positive, not {}".format(other))
        return DeclareArithmeticShiftRight(self.N)(WIDTH=self.N, SHIFTBITS=other)(self)
    elif isinstance(other, Type):
        if not isinstance(other, UIntType):
            raise TypeError("Second argument to arithmetic_shift_right must be a UInt, not {}".format(type(other)))
        return DeclareDynamicArithmeticShiftRight(self.N)(WIDTH=self.N)(self, other)
    else:
        raise TypeError(">> not implemented for argument 2 of type {}".format(
            type(other)))


SIntType.arithmetic_shift_right = arithmetic_shift_right
