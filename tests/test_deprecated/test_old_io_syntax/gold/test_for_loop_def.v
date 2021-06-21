// Defined at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:65
module main (input [1:0] I, output  O);
wire  and2_0_O;
wire  and2_1_O;
wire  and2_2_O;
wire  and2_3_O;
// Instanced at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:69
// Argument I0(I[0]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:71
// Argument I1(I[1]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:72
// Argument O(and2_0_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:74
And2 and2_0 (.I0(I[0]), .I1(I[1]), .O(and2_0_O));
// Instanced at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:69
// Argument I0(and2_0_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:74
// Argument I1(I[1]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:75
// Argument O(and2_1_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:74
And2 and2_1 (.I0(and2_0_O), .I1(I[1]), .O(and2_1_O));
// Instanced at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:69
// Argument I0(and2_1_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:74
// Argument I1(I[1]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:75
// Argument O(and2_2_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:74
And2 and2_2 (.I0(and2_1_O), .I1(I[1]), .O(and2_2_O));
// Instanced at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:69
// Argument I0(and2_2_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:74
// Argument I1(I[1]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:75
// Argument O(and2_3_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:78
And2 and2_3 (.I0(and2_2_O), .I1(I[1]), .O(and2_3_O));
// Wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:78
assign O = and2_3_O;
endmodule

