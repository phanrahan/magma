from magma import *
from magma.backend import verilog

def test_1_bit_logic():
    main = DefineCircuit('main', "a", In(Bit), "b", In(Bit), "c", In(Bit), "d", Out(Bit))
    d = (main.a & main.b) | (main.b ^ ~main.c)
    wire(d, main.d)
    assert verilog.compile(main) == """
module main (input  a, input  b, input  c, output  d);
wire  inst0_O;
wire  inst1_O;
wire  inst2_O;
wire  inst3_O;
And1 inst0 (.I0(a), .I1(b), .O(inst0_O));
Invert1 inst1 (.I(c), .O(inst1_O));
Xor1 inst2 (.I0(b), .I1(inst1_O), .O(inst2_O));
Or1 inst3 (.I0(inst0_O), .I1(inst2_O), .O(inst3_O));
assign d = inst3_O;
endmodule
""".lstrip()
