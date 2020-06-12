from magma import *
from magma.is_definition import isdefinition
import pytest


def test_is_definition():
    class IsDefinition(Circuit):
        name = "this_is_definition"
        IO = ["I", In(Bit), "O", Out(Bit)]
        @classmethod
        def definition(cls):
            wire(cls.I, cls.O)

    assert isdefinition(IsDefinition), "Should be a definition"

    with pytest.warns(DeprecationWarning):
        circ = DefineCircuit('another_definition', 'I', In(Bit), 'O', Out(Bit))
        wire(circ.I, circ.O)
        EndDefine()
    assert isdefinition(circ), "Should be a definition"


def test_is_not_definition():
    class IsDefinition(Circuit):
        name = "this_is_not_definition"
        IO = ["I", In(Bit), "O", Out(Bit)]

    assert not isdefinition(IsDefinition), "Should not be a definition"

    class circ(Circuit):
        name = "another_not_definition"
        io = IO(I=In(Bit), O=Out(Bit))
    assert not isdefinition(circ), "Should not be a definition"
