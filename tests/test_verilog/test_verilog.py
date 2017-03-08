import sys
from magma import *

def test():
    Add = DefineCircuit('Add', 'A', In(Bit), 'B', In(Bit), 'C', Out(Bit))
    Add.verilog = 'C = A ^ B;'
    EndCircuit()

    main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    add = Add()
    add(main.I0, main.I1)
    wire(add.C, main.O)
    EndCircuit()

    compile("build/verilog", main)
    assert magma_check_files_equal(__file__, "build/verilog.v", "gold/verilog.v")
