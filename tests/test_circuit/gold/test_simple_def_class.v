// Defined at tests/test_circuit/test_define.py:30
module Main (input [1:0] I, output  O);
wire  And2_inst0_O;
// Instanced at tests/test_circuit/test_define.py:35
// Argument I0(I[0]) wired at tests/test_circuit/test_define.py:36
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:37
// Argument O(And2_inst0_O) wired at tests/test_circuit/test_define.py:38
And2 And2_inst0 (.I0(I[0]), .I1(I[1]), .O(And2_inst0_O));
// Wired at tests/test_circuit/test_define.py:38
assign O = And2_inst0_O;
endmodule

