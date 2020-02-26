module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module TestReplaceTupleStrKey_comb (
    output O__0,
    output O__1
);
wire bit_const_1_None_out;
corebit_const #(
    .value(1'b1)
) bit_const_1_None (
    .out(bit_const_1_None_out)
);
assign O__0 = bit_const_1_None_out;
assign O__1 = bit_const_1_None_out;
endmodule

module TestReplaceTupleStrKey (
    input CLK,
    output O__0,
    output O__1
);
wire TestReplaceTupleStrKey_comb_inst0_O__0;
wire TestReplaceTupleStrKey_comb_inst0_O__1;
TestReplaceTupleStrKey_comb TestReplaceTupleStrKey_comb_inst0 (
    .O__0(TestReplaceTupleStrKey_comb_inst0_O__0),
    .O__1(TestReplaceTupleStrKey_comb_inst0_O__1)
);
assign O__0 = TestReplaceTupleStrKey_comb_inst0_O__0;
assign O__1 = TestReplaceTupleStrKey_comb_inst0_O__1;
endmodule

