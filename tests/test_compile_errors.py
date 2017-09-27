from magma import *
from magma.compile import MultipleDefinitionException


def test_multiple_definitions():
    class Circ1(Circuit):
        name = "same"
        IO = ['I', In(Bit), 'O', Out(Bit)]

        @classmethod
        def definition(io):
            wire(io.I, io.O)

    class Circ2(Circuit):
        name = "same"
        IO = ['I', In(Bit), 'O', Out(Bit)]

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
        compile('shouldnotmatter', test)
        assert False, "Should throw MultipleDefinitionException"
    except MultipleDefinitionException:
        pass


def test_same_definitions():
    class Circ1(Circuit):
        name = "same"
        IO = ['I', In(Bit), 'O', Out(Bit)]

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
