import sys
from magma import *


def test():
    main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

    wire(main.I, main.O)

    compile("build/inout1", main)
    assert magma_check_files_equal(__file__, "build/inout1.v", "gold/inout1.v")
