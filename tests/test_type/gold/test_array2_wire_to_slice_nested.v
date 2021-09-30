module mantle_sliceArrT__hi4__lo2__tBitIn44 (
    input [3:0] in [3:0],
    output [3:0] out [1:0]
);
assign out[1] = in[3];
assign out[0] = in[2];
endmodule

module mantle_sliceArrT__hi2__lo0__tBitIn44 (
    input [3:0] in [3:0],
    output [3:0] out [1:0]
);
assign out[1] = in[1];
assign out[0] = in[0];
endmodule

module mantle_concatArrT__t0BitIn42__t1BitIn42 (
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
wire [3:0] Concat_inst0_out [3:0];
wire [3:0] Slice_inst0_out [1:0];
wire [3:0] Slice_inst1_out [1:0];
wire [3:0] Concat_inst0_in0 [1:0];
assign Concat_inst0_in0[1] = Slice_inst0_out[1];
assign Concat_inst0_in0[0] = Slice_inst0_out[0];
wire [3:0] Concat_inst0_in1 [1:0];
assign Concat_inst0_in1[1] = Slice_inst1_out[1];
assign Concat_inst0_in1[0] = Slice_inst1_out[0];
mantle_concatArrT__t0BitIn42__t1BitIn42 Concat_inst0 (
    .in0(Concat_inst0_in0),
    .in1(Concat_inst0_in1),
    .out(Concat_inst0_out)
);
wire [3:0] Slice_inst0_in [3:0];
assign Slice_inst0_in[3] = I[3];
assign Slice_inst0_in[2] = I[2];
assign Slice_inst0_in[1] = I[1];
assign Slice_inst0_in[0] = I[0];
mantle_sliceArrT__hi4__lo2__tBitIn44 Slice_inst0 (
    .in(Slice_inst0_in),
    .out(Slice_inst0_out)
);
wire [3:0] Slice_inst1_in [3:0];
assign Slice_inst1_in[3] = I[3];
assign Slice_inst1_in[2] = I[2];
assign Slice_inst1_in[1] = I[1];
assign Slice_inst1_in[0] = I[0];
mantle_sliceArrT__hi2__lo0__tBitIn44 Slice_inst1 (
    .in(Slice_inst1_in),
    .out(Slice_inst1_out)
);
assign O[3] = Concat_inst0_out[3];
assign O[2] = Concat_inst0_out[2];
assign O[1] = Concat_inst0_out[1];
assign O[0] = Concat_inst0_out[0];
endmodule

