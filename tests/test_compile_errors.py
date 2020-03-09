import pytest
from magma import *
from magma.uniquification import MultipleDefinitionException


@pytest.mark.skip("Multiple Definitions no longer supported because we cache on names")
def test_multiple_definitions_are_same():
    class Circ1(Circuit):
        name = "same"
        io = m.IO(I=In(Bit), O=Out(Bit))

        wire(io.I, io.O)

    class Circ2(Circuit):
        name = "same"
        io = m.IO(I=In(Bit), O=Out(Bit))

        wire(io.I, io.O)

    class test(Circuit):
        name = "test"
        io = IO(I=In(Bit), O1=Out(Bit), O2=Out(Bit))
        circ1 = Circ1()
        wire(io.I, circ1.I)
        wire(io.O1, circ1.O)
        circ2 = Circ2()
        wire(io.I, circ2.I)
        wire(io.O2, circ2.O)
    try:
        compile('build/shouldnotmatter', test)
        assert False, "Should throw MultipleDefinitionException"
    except MultipleDefinitionException:
        pass


@pytest.mark.skip("Multiple Definitions no longer supported because we cache on names")
def test_multiple_definitions_are_same_older_def_approach():
    io = m.IO(I=In(Bit), O=Out(Bit))
    class Circ1(Circuit):
        name = "same"
        io = IO(*IO)
        wire(io.I, io.O)
    class Circ2(Circuit):
        name = "same"
        io = IO(*IO)
        wire(io.I, io.O)

    class test(Circuit):
        name = "test"
        io = IO(I=In(Bit), O1=Out(Bit), O2=Out(Bit))
        circ1 = Circ1()
        wire(io.I, circ1.I)
        wire(io.O1, circ1.O)
        circ2 = Circ2()
        wire(io.I, circ2.I)
        wire(io.O2, circ2.O)
    try:
        compile('shouldnotmatter', test)
        assert Circ1 is Circ2
    except MultipleDefinitionException:
        pass


@pytest.mark.skip("Multiple Definitions no longer supported because we cache on names")
def test_same_definitions():
    class Circ1(Circuit):
        name = "same"
        io = m.IO(I=In(Bit), O=Out(Bit))

        wire(io.I, io.O)
    class test(Circuit):
        name = "test"
        io = IO(I=In(Bit), O1=Out(Bit), O2=Out(Bit))
        circ1 = Circ1()
        wire(io.I, circ1.I)
        wire(io.O1, circ1.O)
        circ2 = Circ1()
        wire(io.I, circ2.I)
        wire(io.O2, circ2.O)
    try:
        compile("build/test_same_definition", test)
    except MultipleDefinitionException:
        assert False, "Should not throw MultipleDefinitionException"
