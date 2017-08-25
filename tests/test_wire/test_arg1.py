from magma import *
from magma.tests import magma_check_files_equal


def test():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.I, buf.I)
    wire(buf.O, main.O)

    compile("build/arg1", main)
    assert magma_check_files_equal(__file__, "build/arg1.v", "gold/arg1.v")
