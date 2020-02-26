module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module TestReplaceArrayStrKey_comb (
    output [1:0] O
);
wire [1:0] const_3_2_out;
coreir_const #(
    .value(2'h3),
    .width(2)
) const_3_2 (
    .out(const_3_2_out)
);
assign O = const_3_2_out;
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

