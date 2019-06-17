// Defined at tests/test_circuit/test_define.py:55
module main (input [1:0] I, output  O);
wire  And2_inst0_O;
wire  And2_inst1_O;
wire  And2_inst2_O;
wire  And2_inst3_O;
// Instanced at tests/test_circuit/test_define.py:59
// Argument I0(I[0]) wired at tests/test_circuit/test_define.py:61
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:62
// Argument O(And2_inst0_O) wired at tests/test_circuit/test_define.py:64
And2 And2_inst0 (.I0(I[0]), .I1(I[1]), .O(And2_inst0_O));
// Instanced at tests/test_circuit/test_define.py:59
// Argument I0(And2_inst0_O) wired at tests/test_circuit/test_define.py:64
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:65
// Argument O(And2_inst1_O) wired at tests/test_circuit/test_define.py:64
And2 And2_inst1 (.I0(And2_inst0_O), .I1(I[1]), .O(And2_inst1_O));
// Instanced at tests/test_circuit/test_define.py:59
// Argument I0(And2_inst1_O) wired at tests/test_circuit/test_define.py:64
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:65
// Argument O(And2_inst2_O) wired at tests/test_circuit/test_define.py:64
And2 And2_inst2 (.I0(And2_inst1_O), .I1(I[1]), .O(And2_inst2_O));
// Instanced at tests/test_circuit/test_define.py:59
// Argument I0(And2_inst2_O) wired at tests/test_circuit/test_define.py:64
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:65
// Argument O(And2_inst3_O) wired at tests/test_circuit/test_define.py:68
And2 And2_inst3 (.I0(And2_inst2_O), .I1(I[1]), .O(And2_inst3_O));
// Wired at tests/test_circuit/test_define.py:68
assign O = And2_inst3_O;
endmodule

