from magma.t import Type
from magma.bit import Bit, BitType, In, Out
from magma.array import Bits, BitsType
from magma.circuit import DeclareCircuit
from magma.compatibility import IntegerTypes
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


def type_check_binary_operator(operator):
    """
    For binary operations, the other argument must be the same type
    """
    def type_checked_operator(self, other):
        if type(self) != type(other):
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
def DefineAndN(N):
    T = Bits(N)
    return DeclareCircuit("And{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))


@type_check_binary_operator
def __and__(self, other):
    return DefineAndN(self.N)()(self, other)
BitsType.__and__ = __and__


@lru_cache(maxsize=None)
def DefineOrN(N):
    T = Bits(N)
    return DeclareCircuit("Or{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))


@type_check_binary_operator
def __or__(self, other):
    return DefineOrN(self.N)()(self, other)
BitsType.__or__ = __or__


@lru_cache(maxsize=None)
def DefineXorN(N):
    T = Bits(N)
    return DeclareCircuit("Xor{}".format(N), 'I0', In(T), 'I1', In(T), 'O', Out(T))

@type_check_binary_operator
def __xor__(self, other):
    return DefineXorN(self.N)()(self, other)
BitsType.__xor__ = __xor__


@lru_cache(maxsize=None)
def DefineInvertN(N):
    T = Bits(N)
    return DeclareCircuit("Invert{}".format(N), 'I', In(T), 'O', Out(T))

def __invert__(self):
    return DefineInvertN(self.N)()(self)
BitsType.__invert__ = __invert__


@lru_cache(maxsize=None)
def DefineShiftLeftN(N, amount):
    T = Bits(N)
    return DeclareCircuit("ShiftLeft{}_{}".format(N, amount), 'I', In(T), 'O', Out(T))


@lru_cache(maxsize=None)
def DefineDynamicShiftLeftN(N):
    T = Bits(N)
    i1_type = Bits((N - 1).bit_length())
    return DeclareCircuit("DynamicShiftLeft{}".format(N), 'I0', In(T), 'I1', In(i1_type), 'O', Out(T))

def __lshift__(self, other):
    if isinstance(other, IntegerTypes):
        return DefineShiftLeftN(self.N, other)()(self)
    elif isinstance(other, Type):
        return DefineDynamicShiftLeftN(self.N)()(self, other)
    else:
        raise TypeError("<< not implemented for argument 2 of type {}".format(type(other)))
BitsType.__lshift__ = __lshift__


@lru_cache(maxsize=None)
def DefineShiftRightN(N, amount):
    T = Bits(N)
    return DeclareCircuit("ShiftRight{}_{}".format(N, amount), 'I', In(T), 'O', Out(T))


@lru_cache(maxsize=None)
def DefineDynamicShiftRightN(N):
    T = Bits(N)
    i1_type = Bits((N - 1).bit_length())
    return DeclareCircuit("DynamicShiftRight{}".format(N), 'I0', In(T), 'I1', In(i1_type), 'O', Out(T))

def __rshift__(self, other):
    if isinstance(other, IntegerTypes):
        return DefineShiftRightN(self.N, other)()(self)
    elif isinstance(other, Type):
        return DefineDynamicShiftRightN(self.N)()(self, other)
    else:
        raise TypeError(">> not implemented for argument 2 of type {}".format(type(other)))
BitsType.__rshift__ = __rshift__
