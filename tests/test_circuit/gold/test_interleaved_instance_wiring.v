// Defined at tests/test_circuit/test_define.py:82
module main (input [1:0] I, output  O);
wire  And2_inst0_O;
wire  And2_inst1_O;
wire  And2_inst2_O;
// Instanced at tests/test_circuit/test_define.py:84
// Argument I0(I[0]) wired at tests/test_circuit/test_define.py:87
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:88
// Argument O(And2_inst0_O) wired at tests/test_circuit/test_define.py:89
And2 And2_inst0 (.I0(I[0]), .I1(I[1]), .O(And2_inst0_O));
// Instanced at tests/test_circuit/test_define.py:85
// Argument I0(And2_inst0_O) wired at tests/test_circuit/test_define.py:89
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:90
// Argument O(And2_inst1_O) wired at tests/test_circuit/test_define.py:92
And2 And2_inst1 (.I0(And2_inst0_O), .I1(I[1]), .O(And2_inst1_O));
// Instanced at tests/test_circuit/test_define.py:91
// Argument I0(And2_inst1_O) wired at tests/test_circuit/test_define.py:92
// Argument I1(I[0]) wired at tests/test_circuit/test_define.py:93
// Argument O(And2_inst2_O) wired at tests/test_circuit/test_define.py:95
And2 And2_inst2 (.I0(And2_inst1_O), .I1(I[0]), .O(And2_inst2_O));
// Wired at tests/test_circuit/test_define.py:95
assign O = And2_inst2_O;
endmodule

