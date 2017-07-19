from magma import *
from magma.backend import verilog

def test_1_bit_logic():
    class TestCircuit(Circuit):
        name = "test_circuit"
        IO = ["a", In(Bit), "b", In(Bit), "c", In(Bit), "d", Out(Bit)]
        @classmethod
        def definition(circuit):
            d = (circuit.a & circuit.b) | (circuit.b ^ ~circuit.c)
            wire(d, circuit.d)
    assert verilog.compile(TestCircuit) == """
module test_circuit (input  a, input  b, input  c, output  d);
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

def test_bits_logic():
    class TestCircuit(Circuit):
        name = "test_circuit"
        IO = ["a", In(Bits(8)), "b", In(Bits(8)), "c", In(Bits(8)), "d", In(Bits(3)), "e", Out(Bits(8))]
        @classmethod
        def definition(circuit):
            print(type(circuit.a))
            e = (circuit.a & circuit.b) | (circuit.b ^ ~circuit.c) >> 3 >> circuit.d << 3 << circuit.d
            wire(e, circuit.e)
    assert verilog.compile(TestCircuit) == """
module test_circuit (input [7:0] a, input [7:0] b, input [7:0] c, input [2:0] d, output [7:0] e);
wire [7:0] inst0_O;
wire [7:0] inst1_O;
wire [7:0] inst2_O;
wire [7:0] inst3_O;
wire [7:0] inst4_O;
wire [7:0] inst5_O;
wire [7:0] inst6_O;
wire [7:0] inst7_O;
And8 inst0 (.I0(a), .I1(b), .O(inst0_O));
Invert8 inst1 (.I(c), .O(inst1_O));
Xor8 inst2 (.I0(b), .I1(inst1_O), .O(inst2_O));
ShiftRight8_3 inst3 (.I(inst2_O), .O(inst3_O));
DynamicShiftRight8 inst4 (.I0(inst3_O), .I1(d), .O(inst4_O));
ShiftLeft8_3 inst5 (.I(inst4_O), .O(inst5_O));
DynamicShiftLeft8 inst6 (.I0(inst5_O), .I1(d), .O(inst6_O));
Or8 inst7 (.I0(inst0_O), .I1(inst6_O), .O(inst7_O));
assign e = inst7_O;
endmodule

""".lstrip()
