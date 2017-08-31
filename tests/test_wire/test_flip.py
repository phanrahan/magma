from magma import *
from magma.tests import magma_check_files_equal


def test():
    Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "O", Out(Bit))

    buf = Buf()

    # flip inputs and outputs
    wire(buf.I, bit(1))
    wire(main.O, buf.O)

    compile("build/flip", main)
    assert magma_check_files_equal(__file__, "build/flip.v", "gold/flip.v")
