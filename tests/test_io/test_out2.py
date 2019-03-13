from magma import *
from magma.testing import check_files_equal


def test():
    main = DefineCircuit("main", "O", Out(Bits[2]))

    wire(array([0,1]), main.O)

    compile("build/out2", main)
    assert check_files_equal(__file__, "build/out2.v", "gold/out2.v")
