from magma import *
from magma.tests import magma_check_files_equal


def test():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "O", Out(Bit))

    buf = Buf()

    wire(0, buf.I)
    wire(buf.O, main.O)

    compile("build/const0", main)
    assert magma_check_files_equal(__file__, "build/const0.v", "gold/const0.v")
