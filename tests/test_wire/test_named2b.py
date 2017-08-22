import sys
from magma import *


def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I", In(Bits(2)), "O", Out(Bit))

    a = And2()

    a(I0=main.I[0])
    a(I1=main.I[1])
    wire(a.O, main.O)

    compile("build/named2b", main)
    assert magma_check_files_equal(__file__, "build/named2b.v", "gold/named2b.v")
