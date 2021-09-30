module mantle_sliceArrT__hi2__lo1__tBitIn2 (
    input [1:0] in,
    output [0:0] out
);
assign out = in[1];
endmodule

module mantle_sliceArrT__hi1__lo0__tBitIn2 (
    input [1:0] in,
    output [0:0] out
);
assign out = in[0];
endmodule

module coreir_concat #(
    parameter width0 = 1,
    parameter width1 = 1
) (
    input [width0-1:0] in0,
    input [width1-1:0] in1,
    output [width0+width1-1:0] out
);
  assign out = {in1,in0};
endmodule

module Foo (
    input [1:0] I,
    output [1:0] O
);
wire [1:0] Concat_inst0_out;
wire [0:0] Slice_inst0_out;
wire [0:0] Slice_inst1_out;
coreir_concat #(
    .width0(1),
    .width1(1)
) Concat_inst0 (
    .in0(Slice_inst0_out),
    .in1(Slice_inst1_out),
    .out(Concat_inst0_out)
);
mantle_sliceArrT__hi2__lo1__tBitIn2 Slice_inst0 (
    .in(I),
    .out(Slice_inst0_out)
);
mantle_sliceArrT__hi1__lo0__tBitIn2 Slice_inst1 (
    .in(I),
    .out(Slice_inst1_out)
);
assign O = Concat_inst0_out;
endmodule

