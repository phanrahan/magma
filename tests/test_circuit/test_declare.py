import sys
from magma import *

def test(): 
    main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

    And2 = DeclareCircuit(*(['And2', 'output', Out(Bit)] + 2 * ['input', In(Bit)]))
    and2 = And2()

    main.O(and2(main.I0,main.I1))

    compile("build/declare", main)

    assert magma_check_files_equal(__file__, "build/declare.v", "gold/declare.v")
