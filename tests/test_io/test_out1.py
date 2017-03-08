import sys
from magma import *


def test():
    main = DefineCircuit("main", "O", Out(Bit))

    wire(1, main.O)

    compile("build/out1", main)
    assert magma_check_files_equal(__file__, "build/out1.v", "gold/out1.v")
