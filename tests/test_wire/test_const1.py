from magma import *
from magma.tests import magma_check_files_equal


def test():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "O", Out(Bit))

    buf = Buf()

    wire(1, buf.I)
    wire(buf.O, main.O)

    compile("build/const1", main)
    assert magma_check_files_equal(__file__, "build/const1.v", "gold/const1.v")


