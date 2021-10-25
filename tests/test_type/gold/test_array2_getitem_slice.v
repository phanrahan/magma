module mantle_sliceArrT__hi4__lo2__tBitIn4 (
    input [3:0] in,
    output [1:0] out
);
assign out = {in[3],in[2]};
endmodule

module mantle_sliceArrT__hi2__lo0__tBitIn4 (
    input [3:0] in,
    output [1:0] out
);
assign out = {in[1],in[0]};
endmodule

module mantle_concatNArrT__Ns22__t_childBitIn (
    input [1:0] in0,
    input [1:0] in1,
    output [3:0] out
);
assign out = {in1[1],in1[0],in0[1],in0[0]};
endmodule

module Foo (
    input [3:0] I,
    output [3:0] O
);
wire [3:0] ConcatN_inst0_out;
wire [1:0] Slice_inst0_out;
wire [1:0] Slice_inst1_out;
mantle_concatNArrT__Ns22__t_childBitIn ConcatN_inst0 (
    .in0(Slice_inst0_out),
    .in1(Slice_inst1_out),
    .out(ConcatN_inst0_out)
);
mantle_sliceArrT__hi4__lo2__tBitIn4 Slice_inst0 (
    .in(I),
    .out(Slice_inst0_out)
);
mantle_sliceArrT__hi2__lo0__tBitIn4 Slice_inst1 (
    .in(I),
    .out(Slice_inst1_out)
);
assign O = ConcatN_inst0_out;
endmodule

