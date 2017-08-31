from magma import *
from magma.testing import check_files_equal


def test_const0():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "O", Out(Bit))

    buf = Buf()

    wire(0, buf.I)
    wire(buf.O, main.O)

    compile("build/const0", main)
    assert check_files_equal(__file__, "build/const0.v", "gold/const0.v")


def test_const1():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "O", Out(Bit))

    buf = Buf()

    wire(1, buf.I)
    wire(buf.O, main.O)

    compile("build/const1", main)
    assert check_files_equal(__file__, "build/const1.v", "gold/const1.v")


