module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module TestReplaceArrayStrKey_comb (
    output [1:0] O
);
wire bit_const_1_None_out;
corebit_const #(
    .value(1'b1)
) bit_const_1_None (
    .out(bit_const_1_None_out)
);
assign O = {bit_const_1_None_out,bit_const_1_None_out};
endmodule

module TestReplaceArrayStrKey (
    input CLK,
    output [1:0] O
);
wire [1:0] TestReplaceArrayStrKey_comb_inst0_O;
TestReplaceArrayStrKey_comb TestReplaceArrayStrKey_comb_inst0 (
    .O(TestReplaceArrayStrKey_comb_inst0_O)
);
assign O = TestReplaceArrayStrKey_comb_inst0_O;
endmodule

