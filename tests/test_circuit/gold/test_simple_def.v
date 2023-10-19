// Defined at tests/test_circuit/test_define.py:18
module main (input [1:0] I, output  O);
wire  and2_O;
// Instanced at tests/test_circuit/test_define.py:21
// Argument I0(I[0]) wired at tests/test_circuit/test_define.py:23
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:24
// Argument O(and2_O) wired at tests/test_circuit/test_define.py:25
And2 and2 (.I0(I[0]), .I1(I[1]), .O(and2_O));
// Wired at tests/test_circuit/test_define.py:25
assign O = and2_O;
endmodule

