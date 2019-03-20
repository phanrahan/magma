from magma import *
from magma.testing import check_files_equal


def test():
    main = DefineCircuit("main", "I", In(Bits[2]), "O", Out(Bits[2]))

    wire(main.I, main.O)

    compile("build/inout2", main)
    assert check_files_equal(__file__, "build/inout2.v", "gold/inout2.v")
