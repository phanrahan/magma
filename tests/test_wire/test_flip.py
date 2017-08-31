from magma import *
from magma.testing import check_files_equal


def test():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "O", Out(Bit))

    buf = Buf()

    # flip inputs and outputs
    wire(buf.I, bit(1))
    wire(main.O, buf.O)

    compile("build/flip", main)
    assert check_files_equal(__file__, "build/flip.v", "gold/flip.v")
