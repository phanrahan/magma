from magma import *
from magma.is_definition import isdefinition


def test_is_definition():
    class IsDefinition(Circuit):
        name = "this_is_definition"
        io = m.IO(I=In(Bit), O=Out(Bit))
        wire(io.I, io.O)

    assert isdefinition(IsDefinition), "Should be a definition"

    circ = DefineCircuit('another_definition', 'I', In(Bit), 'O', Out(Bit))
    wire(circ.I, circ.O)
    EndDefine()
    assert isdefinition(circ), "Should be a definition"


def test_is_not_definition():
    class IsDefinition(Circuit):
        name = "this_is_not_definition"
        io = m.IO(I=In(Bit), O=Out(Bit))

    assert not isdefinition(IsDefinition), "Should not be a definition"

    circ = DeclareCircuit('another_not_definition', 'I', In(Bit), 'O', Out(Bit))
    assert not isdefinition(circ), "Should not be a definition"
