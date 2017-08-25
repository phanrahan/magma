from magma import *
from magma.tests import magma_check_files_equal


def test():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.I, buf[0])
    wire(buf[1], main.O)

    compile("build/pos", main)
    assert magma_check_files_equal(__file__, "build/pos.v", "gold/pos.v")
