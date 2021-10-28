module mantle_slicesArrT__slices4220__tBitIn44 (
    input [3:0] in [3:0],
    output [3:0] out0 [1:0],
    output [3:0] out1 [1:0]
);
assign out0[1] = in[3];
assign out0[0] = in[2];
assign out1[1] = in[1];
assign out1[0] = in[0];
endmodule

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
wire [3:0] SlicesBuilder_out0 [1:0];
wire [3:0] SlicesBuilder_out1 [1:0];
wire [3:0] ConcatN_inst0_in0 [1:0];
assign ConcatN_inst0_in0[1] = SlicesBuilder_out0[1];
assign ConcatN_inst0_in0[0] = SlicesBuilder_out0[0];
wire [3:0] ConcatN_inst0_in1 [1:0];
assign ConcatN_inst0_in1[1] = SlicesBuilder_out1[1];
assign ConcatN_inst0_in1[0] = SlicesBuilder_out1[0];
mantle_concatNArrT__Ns22__t_childBitIn4 ConcatN_inst0 (
    .in0(ConcatN_inst0_in0),
    .in1(ConcatN_inst0_in1),
    .out(ConcatN_inst0_out)
);
wire [3:0] SlicesBuilder_in [3:0];
assign SlicesBuilder_in[3] = I[3];
assign SlicesBuilder_in[2] = I[2];
assign SlicesBuilder_in[1] = I[1];
assign SlicesBuilder_in[0] = I[0];
mantle_slicesArrT__slices4220__tBitIn44 SlicesBuilder (
    .in(SlicesBuilder_in),
    .out0(SlicesBuilder_out0),
    .out1(SlicesBuilder_out1)
);
assign O[3] = ConcatN_inst0_out[3];
assign O[2] = ConcatN_inst0_out[2];
assign O[1] = ConcatN_inst0_out[1];
assign O[0] = ConcatN_inst0_out[0];
endmodule

