// Defined at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:38
module Main (input [1:0] I, output  O);
wire  and2_O;
// Instanced at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:43
// Argument I0(I[0]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:44
// Argument I1(I[1]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:45
// Argument O(and2_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:46
And2 and2 (.I0(I[0]), .I1(I[1]), .O(and2_O));
// Wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:46
assign O = and2_O;
endmodule

