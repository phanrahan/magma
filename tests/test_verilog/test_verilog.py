import sys
from magma import *
from magma import DeclareFromVerilog, DeclareFromTemplatedVerilog

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

@pytest.mark.skipif(sys.version_info < (3, 0), reason="requires Python3")
def test_from_verilog():

    source = '''\
module CSA_4 ( input [3:0] a,b,c, output [3:0] s, co);
   assign s = a ^ b ^c;
   assign co = a&b | b&c | a&c;
endmodule'''

    modules = DeclareFromVerilog(source)

    assert len(modules) == 1
    m = modules[0]

    assert m.name == 'CSA_4'
    assert str(m.IO) == 'Interface[a, Array(4,In(Bit)), b, Array(4,In(Bit)), c, Array(4,In(Bit)), s, Array(4,Out(Bit)), co, Array(4,Out(Bit))]'

@pytest.mark.skipif(sys.version_info < (3, 0), reason="requires Python3")
def test_from_templated_verilog():
    source = '''\
module CSA_${N} ( input [${N-1}:0] a,b,c, output [${N-1}:0] s, co);
   assign s = a ^ b ^c;
   assign co = a&b | b&c | a&c;
endmodule'''

    modules = DeclareFromTemplatedVerilog(source, N=4)

    assert len(modules) == 1
    m = modules[0]

    assert m.name == 'CSA_4'
    assert str(m.IO) == 'Interface[a, Array(4,In(Bit)), b, Array(4,In(Bit)), c, Array(4,In(Bit)), s, Array(4,Out(Bit)), co, Array(4,Out(Bit))]'

