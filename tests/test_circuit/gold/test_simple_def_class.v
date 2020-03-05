// Defined at tests/test_circuit/test_define.py:34
module Main (input [1:0] I, output  O);
wire  and2_O;
// Instanced at tests/test_circuit/test_define.py:37
// Argument I0(I[0]) wired at tests/test_circuit/test_define.py:38
// Argument I1(I[1]) wired at tests/test_circuit/test_define.py:39
// Argument O(and2_O) wired at tests/test_circuit/test_define.py:40
And2 and2 (.I0(I[0]), .I1(I[1]), .O(and2_O));
// Wired at tests/test_circuit/test_define.py:40
assign O = and2_O;
endmodule

