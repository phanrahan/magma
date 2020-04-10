module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module TestReplaceArray_comb (
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

module TestReplaceArray (
    input CLK,
    output [1:0] O
);
wire [1:0] TestReplaceArray_comb_inst0_O;
TestReplaceArray_comb TestReplaceArray_comb_inst0 (
    .O(TestReplaceArray_comb_inst0_O)
);
assign O = TestReplaceArray_comb_inst0_O;
endmodule

