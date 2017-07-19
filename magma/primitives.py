from magma.bit import Bit, BitType, In, Out
from magma.circuit import DeclareCircuit
from functools import lru_cache


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
