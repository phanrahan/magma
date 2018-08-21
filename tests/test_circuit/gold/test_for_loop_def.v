// Defined at tests/test_circuit/test_define.py:37
module main (input [1:0] I, output  O);
wire  inst0_O;
wire  inst1_O;
wire  inst2_O;
wire  inst3_O;
And2 inst0 (.I0(I[0]), .I1(I[1]), .O(inst0_O)); // Instanced at tests/test_circuit/test_define.py:41
And2 inst1 (.I0(inst0_O), .I1(I[1]), .O(inst1_O)); // Instanced at tests/test_circuit/test_define.py:41
And2 inst2 (.I0(inst1_O), .I1(I[1]), .O(inst2_O)); // Instanced at tests/test_circuit/test_define.py:41
And2 inst3 (.I0(inst2_O), .I1(I[1]), .O(inst3_O)); // Instanced at tests/test_circuit/test_define.py:41
assign O = inst3_O;  // Wired at tests/test_circuit/test_define.py:50
endmodule

