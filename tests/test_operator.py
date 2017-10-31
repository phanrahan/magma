from magma import *
from magma.operator import OperatorMantleNotImportedError


def test_error():
    circ = DefineCircuit("test", "a", In(Bits(4)), "b", Out(Bits(4)))
    try:
        b = ~circ.a
        assert False, "Operator should throw an error since mantle is not imported"
    except OperatorMantleNotImportedError as e:
        pass
