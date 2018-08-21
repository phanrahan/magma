// Defined at tests/test_circuit/test_define.py:67
module main (input [1:0] I, output  O);
wire  inst0_O;
wire  inst1_O;
wire  inst2_O;
// Instanced at tests/test_circuit/test_define.py:69
// Argument I0(I[0]) wired at tests/test_circuit/test_define.py:72
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:73
// Argument O(inst0_O) wired at tests/test_circuit/test_define.py:74
And2 inst0 (.I0(I[0]), .I1(I[1]), .O(inst0_O));
// Instanced at tests/test_circuit/test_define.py:70
// Argument I0(inst0_O) wired at tests/test_circuit/test_define.py:74
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:75
// Argument O(inst1_O) wired at tests/test_circuit/test_define.py:77
And2 inst1 (.I0(inst0_O), .I1(I[1]), .O(inst1_O));
// Instanced at tests/test_circuit/test_define.py:76
// Argument I0(inst1_O) wired at tests/test_circuit/test_define.py:77
// Argument I1(I[0]) wired at tests/test_circuit/test_define.py:78
// Argument O(inst2_O) wired at tests/test_circuit/test_define.py:80
And2 inst2 (.I0(inst1_O), .I1(I[0]), .O(inst2_O));
// Wired at tests/test_circuit/test_define.py:80
assign O = inst2_O;
endmodule

