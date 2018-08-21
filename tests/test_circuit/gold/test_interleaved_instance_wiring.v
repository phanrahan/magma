module main (input [1:0] I, output  O);
Defined at tests/test_circuit/test_define.py:67wire  inst0_O;
wire  inst1_O;
wire  inst2_O;
And2 inst0 (.I0(I[0]), .I1(I[1]), .O(inst0_O)); // Instanced at tests/test_circuit/test_define.py:69
And2 inst1 (.I0(inst0_O), .I1(I[1]), .O(inst1_O)); // Instanced at tests/test_circuit/test_define.py:70
And2 inst2 (.I0(inst1_O), .I1(I[0]), .O(inst2_O)); // Instanced at tests/test_circuit/test_define.py:76
assign O = inst2_O;  // Wired at tests/test_circuit/test_define.py:80
endmodule

