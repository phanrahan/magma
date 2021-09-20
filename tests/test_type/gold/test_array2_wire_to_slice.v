module coreir_slice #(
    parameter hi = 1,
    parameter lo = 0,
    parameter width = 1
) (
    input [width-1:0] in,
    output [hi-lo-1:0] out
);
  assign out = in[hi-1:lo];
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
    input [3:0] I,
    output [3:0] O
);
wire [3:0] Concat_inst0_out;
wire [1:0] Slice_inst0_out;
wire [1:0] Slice_inst1_out;
coreir_concat #(
    .width0(2),
    .width1(2)
) Concat_inst0 (
    .in0(Slice_inst0_out),
    .in1(Slice_inst1_out),
    .out(Concat_inst0_out)
);
coreir_slice #(
    .hi(4),
    .lo(2),
    .width(4)
) Slice_inst0 (
    .in(I),
    .out(Slice_inst0_out)
);
coreir_slice #(
    .hi(2),
    .lo(0),
    .width(4)
) Slice_inst1 (
    .in(I),
    .out(Slice_inst1_out)
);
assign O = Concat_inst0_out;
endmodule

