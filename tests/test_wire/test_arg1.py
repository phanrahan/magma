from magma import *
from magma.testing import check_files_equal


def test():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    buf = Buf()
    wire(main.I, buf.I)
    wire(buf.O, main.O)

    compile("build/arg1", main)
    assert check_files_equal(__file__, "build/arg1.v", "gold/arg1.v")
