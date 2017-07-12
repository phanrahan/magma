import os
from magma.bit import BitType

mode = os.environ.get("MAGMA_PRIMITIVES", "FIRRTL")


def type_check_binary_operator(operator):
    """
    For Binary Bit operations, the other argument must be a bit
    """
    def type_checked_operator(self, other):
        if not isinstance(other, BitType):
            raise TypeError("unsupported operand type(s) for {}: '{}' and"
                    "'{}'".format(operator.__name__, type(self), type(other)))
        return operator(self, other)
    return type_checked_operator


if mode == "FIRRTL":
    from magma.primitives.firrtl import *
else:
    raise NotImplementedError()

@type_check_binary_operator
def __and__(self, other):
    return And(1)(self, other)[0]
BitType.__and__ = __and__
