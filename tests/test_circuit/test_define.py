import sys
from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    I = array(main.I0, main.I1)
    O = main.O

    AndN2 = DefineCircuit("And2", "I", In(Array2), "O", Out(Bit) )

    and2 = And2()

    wire( AndN2.I[0], and2.I0 )
    wire( AndN2.I[1], and2.I1 )
    wire( and2.O, AndN2.O )

    EndCircuit()


    and2 = AndN2()

    O( and2(I) )

    compile("build/define", main)

    assert magma_check_files_equal(__file__, "build/define.v", "gold/define.v")
