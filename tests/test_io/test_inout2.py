import sys
from magma import *


def test():
    main = DefineCircuit("main", "I", In(Array2), "O", Out(Array2))

    wire(main.I, main.O)

    compile("build/inout2", main)
    assert magma_check_files_equal(__file__, "build/inout2.v", "gold/inout2.v")
