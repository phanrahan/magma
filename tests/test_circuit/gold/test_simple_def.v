module main (input [1:0] I, output  O);
wire  inst0_O;
And2 inst0 (.I0(I[0]), .I1(I[1]), .O(inst0_O)); // Instanced at tests/test_circuit/test_define.py:16
assign O = inst0_O;  // Wired at tests/test_circuit/test_define.py:20
endmodule

