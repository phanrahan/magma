module mantle_slicesArrT__slices2110__tBitIn2 (
    input [1:0] in,
    output [0:0] out0,
    output [0:0] out1
);
assign out0 = in[1];
assign out1 = in[0];
endmodule

module mantle_concatNArrT__Ns11__t_childBitIn (
    input [0:0] in0,
    input [0:0] in1,
    output [1:0] out
);
assign out = {in1[0],in0[0]};
endmodule

module Foo (
    input [1:0] I,
    output [1:0] O
);
wire [1:0] ConcatN_inst0_out;
wire [0:0] SliceBuilder_out0;
wire [0:0] SliceBuilder_out1;
mantle_concatNArrT__Ns11__t_childBitIn ConcatN_inst0 (
    .in0(SliceBuilder_out0),
    .in1(SliceBuilder_out1),
    .out(ConcatN_inst0_out)
);
mantle_slicesArrT__slices2110__tBitIn2 SliceBuilder (
    .in(I),
    .out0(SliceBuilder_out0),
    .out1(SliceBuilder_out1)
);
assign O = ConcatN_inst0_out;
endmodule

