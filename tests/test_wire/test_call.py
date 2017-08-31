from magma import *
from magma.testing import check_files_equal


def test_call1():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    a = And2()

    a( main.I0, main.I1 )
    wire(a, main.O)

    compile("build/call1", main)
    assert check_files_equal(__file__, "build/call1.v", "gold/call1.v")


def test_call2():
    def DefineAndN(n):
        name = 'AndN%d' % n
        return DeclareCircuit(name, "I", In(Bits(n)), "O", Out(Bit))

    def AndN(n):
        return DefineAndN(n)()

    main = DefineCircuit("main", "I", In(Bits(2)), "O", Out(Bit))

    a = AndN(2)

    a( main.I )
    wire(a, main.O)

    compile("build/call2", main)
    assert check_files_equal(__file__, "build/call2.v", "gold/call2.v")
