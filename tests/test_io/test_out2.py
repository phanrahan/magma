import sys
from magma import *


def test():
    main = DefineCircuit("main", "O", Out(Array2))

    wire(array(0,1), main.O)

    compile("build/out2", main)
    assert magma_check_files_equal(__file__, "build/out2.v", "gold/out2.v")
