// Defined at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:89
module main (input [1:0] I, output  O);
wire  and2_0_O;
wire  and2_1_O;
wire  and2_2_O;
// Instanced at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:91
// Argument I0(I[0]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:94
// Argument I1(I[1]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:95
// Argument O(and2_0_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:96
And2 and2_0 (.I0(I[0]), .I1(I[1]), .O(and2_0_O));
// Instanced at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:92
// Argument I0(and2_0_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:96
// Argument I1(I[1]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:97
// Argument O(and2_1_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:99
And2 and2_1 (.I0(and2_0_O), .I1(I[1]), .O(and2_1_O));
// Instanced at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:98
// Argument I0(and2_1_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:99
// Argument I1(I[0]) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:100
// Argument O(and2_2_O) wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:102
And2 and2_2 (.I0(and2_1_O), .I1(I[0]), .O(and2_2_O));
// Wired at tests/test_deprecated/test_old_io_syntax/test_old_io_syntax_define.py:102
assign O = and2_2_O;
endmodule

