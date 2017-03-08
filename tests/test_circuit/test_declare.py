import sys
from magma import *

def test(): 
    main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    I0 = main.I0
    I1 = main.I1
    O = main.O

    And2 = DeclareCircuit(*(['And2', 'output', Out(Bit)] + 2 * ['input', In(Bit)]))
    and2 = And2()

    O(and2(I0,I1))

    compile("build/declare", main)

    assert magma_check_files_equal(__file__, "build/declare.v", "gold/declare.v")
