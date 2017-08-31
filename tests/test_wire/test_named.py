from magma import *
from magma.testing import check_files_equal


def test_named1():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    buf(I=main.I)
    wire(buf.O, main.O)

    compile("build/named1", main)
    assert check_files_equal(__file__, "build/named1.v", "gold/named1.v")

def test_named2():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bits(2)), "O", Out(Bit))

    a = And2()

    a(I0=main.I[0], I1=main.I[1])
    wire(a.O, main.O)

    compile("build/named2a", main)
    assert check_files_equal(__file__, "build/named2a.v", "gold/named2a.v")

def test_named3():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bits(2)), "O", Out(Bit))

    a = And2()

    a(I0=main.I[0])
    a(I1=main.I[1])
    wire(a.O, main.O)

    compile("build/named2b", main)
    assert check_files_equal(__file__, "build/named2b.v", "gold/named2b.v")


def test_named4():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bits(2)), "O", Out(Bit))

    a = And2()

    a(I1=main.I[1])
    a(I0=main.I[0])
    wire(a.O, main.O)

    compile("build/named2c", main)
    assert check_files_equal(__file__, "build/named2c.v", "gold/named2c.v")
