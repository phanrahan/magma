// Defined at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:23
module main (input [1:0] I, output  O);
wire  and2_O;
// Instanced at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:25
// Argument I0(I[0]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:27
// Argument I1(I[1]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:28
// Argument O(and2_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:29
And2 and2 (.I0(I[0]), .I1(I[1]), .O(and2_O));
// Wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:29
assign O = and2_O;
endmodule

