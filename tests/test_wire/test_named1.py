from magma import *
from magma.testing import check_files_equal


def test():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    buf(I=main.I)
    wire(buf.O, main.O)

    compile("build/named1", main)
    assert check_files_equal(__file__, "build/named1.v", "gold/named1.v")

