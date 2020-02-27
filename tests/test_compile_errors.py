import pytest
from magma import *
from magma.uniquification import MultipleDefinitionException


@pytest.mark.skip("Multiple Definitions no longer supported because we cache on names")
def test_multiple_definitions_are_same():
    class Circ1(Circuit):
        name = "same"
        io = m.IO('I', In(Bit), 'O', Out(Bit))

        @classmethod
        def definition(io):
            wire(io.I, io.O)

    class Circ2(Circuit):
        name = "same"
        io = m.IO('I', In(Bit), 'O', Out(Bit))

        @classmethod
        def definition(io):
            wire(io.I, io.O)

    test = DefineCircuit('test', 'I', In(Bit), 'O1', Out(Bit), 'O2', Out(Bit))
    circ1 = Circ1()
    wire(test.I, circ1.I)
    wire(test.O1, circ1.O)
    circ2 = Circ2()
    wire(test.I, circ2.I)
    wire(test.O2, circ2.O)
    EndDefine()
    try:
        compile('build/shouldnotmatter', test)
        assert False, "Should throw MultipleDefinitionException"
    except MultipleDefinitionException:
        pass


@pytest.mark.skip("Multiple Definitions no longer supported because we cache on names")
def test_multiple_definitions_are_same_older_def_approach():
    io = m.IO('I', In(Bit), 'O', Out(Bit))
    Circ1 = DefineCircuit("same", *IO)
    wire(Circ1.I, Circ1.O)
    EndDefine()
    Circ2 = DefineCircuit("same", *IO)
    wire(Circ2.I, Circ2.O)
    EndDefine()

    test = DefineCircuit('test', 'I', In(Bit), 'O1', Out(Bit), 'O2', Out(Bit))
    circ1 = Circ1()
    wire(test.I, circ1.I)
    wire(test.O1, circ1.O)
    circ2 = Circ2()
    wire(test.I, circ2.I)
    wire(test.O2, circ2.O)
    EndDefine()
    try:
        compile('shouldnotmatter', test)
        assert Circ1 is Circ2
    except MultipleDefinitionException:
        pass


@pytest.mark.skip("Multiple Definitions no longer supported because we cache on names")
def test_same_definitions():
    class Circ1(Circuit):
        name = "same"
        io = m.IO('I', In(Bit), 'O', Out(Bit))

        @classmethod
        def definition(io):
            wire(io.I, io.O)
    test = DefineCircuit('test', 'I', In(Bit), 'O1', Out(Bit), 'O2', Out(Bit))
    circ1 = Circ1()
    wire(test.I, circ1.I)
    wire(test.O1, circ1.O)
    circ2 = Circ1()
    wire(test.I, circ2.I)
    wire(test.O2, circ2.O)
    EndDefine()
    try:
        compile("build/test_same_definition", test)
    except MultipleDefinitionException:
        assert False, "Should not throw MultipleDefinitionException"
