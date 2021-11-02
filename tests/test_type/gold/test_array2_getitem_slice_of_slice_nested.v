module mantle_concatNArrT__Ns22__t_childBitIn4 (
    input [3:0] in0 [1:0],
    input [3:0] in1 [1:0],
    output [3:0] out [3:0]
);
assign out[3] = in1[1];
assign out[2] = in1[0];
assign out[1] = in0[1];
assign out[0] = in0[0];
endmodule

module Foo (
    input [3:0] I [3:0],
    output [3:0] O [3:0]
);
wire [3:0] ConcatN_inst0_out [3:0];
wire [3:0] ConcatN_inst0_in0 [1:0];
assign ConcatN_inst0_in0[1] = I[2];
assign ConcatN_inst0_in0[0] = I[1];
wire [3:0] ConcatN_inst0_in1 [1:0];
assign ConcatN_inst0_in1[1] = I[2];
assign ConcatN_inst0_in1[0] = I[1];
mantle_concatNArrT__Ns22__t_childBitIn4 ConcatN_inst0 (
    .in0(ConcatN_inst0_in0),
    .in1(ConcatN_inst0_in1),
    .out(ConcatN_inst0_out)
);
assign O[3] = ConcatN_inst0_out[3];
assign O[2] = ConcatN_inst0_out[2];
assign O[1] = ConcatN_inst0_out[1];
assign O[0] = ConcatN_inst0_out[0];
endmodule

