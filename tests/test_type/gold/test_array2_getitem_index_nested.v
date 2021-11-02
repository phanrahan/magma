module mantle_concatNArrT__Ns11__t_childBitIn2 (
    input [1:0] in0 [0:0],
    input [1:0] in1 [0:0],
    output [1:0] out [1:0]
);
assign out[1] = in1[0];
assign out[0] = in0[0];
endmodule

module Foo (
    input [1:0] I [1:0],
    output [1:0] O [1:0]
);
wire [1:0] ConcatN_inst0_out [1:0];
wire [1:0] ConcatN_inst0_in0 [0:0];
assign ConcatN_inst0_in0[0] = I[1];
wire [1:0] ConcatN_inst0_in1 [0:0];
assign ConcatN_inst0_in1[0] = I[0];
mantle_concatNArrT__Ns11__t_childBitIn2 ConcatN_inst0 (
    .in0(ConcatN_inst0_in0),
    .in1(ConcatN_inst0_in1),
    .out(ConcatN_inst0_out)
);
assign O[1] = ConcatN_inst0_out[1];
assign O[0] = ConcatN_inst0_out[0];
endmodule

