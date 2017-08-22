import sys
from magma import *


def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bits(2)), "O", Out(Bit))

    a = And2()

    wire( main.I[0], a.I0 )
    wire( main.I[1], a.I1 )
    wire(a.O, main.O)

    compile("build/arg2", main)
    assert magma_check_files_equal(__file__, "build/arg2.v", "gold/arg2.v")
