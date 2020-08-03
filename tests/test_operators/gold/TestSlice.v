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

module coreir_mux #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    input sel,
    output [width-1:0] out
);
  assign out = sel ? in1 : in0;
endmodule

module commonlib_muxn__N2__width6 (
    input [1:0][5:0] in_data,
    input [0:0] in_sel,
    output [5:0] out
);
wire [5:0] _join_out;
coreir_mux #(
    .width(6)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module commonlib_muxn__N4__width6 (
    input [3:0][5:0] in_data,
    input [1:0] in_sel,
    output [5:0] out
);
wire [5:0] _join_out;
wire [5:0] muxN_0_out;
wire [5:0] muxN_1_out;
wire [0:0] sel_slice0_out;
wire [0:0] sel_slice1_out;
coreir_mux #(
    .width(6)
) _join (
    .in0(muxN_0_out),
    .in1(muxN_1_out),
    .sel(in_sel[1]),
    .out(_join_out)
);
commonlib_muxn__N2__width6 muxN_0 (
    .in_data({in_data[1],in_data[0]}),
    .in_sel(sel_slice0_out),
    .out(muxN_0_out)
);
commonlib_muxn__N2__width6 muxN_1 (
    .in_data({in_data[3],in_data[2]}),
    .in_sel(sel_slice1_out),
    .out(muxN_1_out)
);
coreir_slice #(
    .hi(1),
    .lo(0),
    .width(2)
) sel_slice0 (
    .in(in_sel),
    .out(sel_slice0_out)
);
coreir_slice #(
    .hi(1),
    .lo(0),
    .width(2)
) sel_slice1 (
    .in(in_sel),
    .out(sel_slice1_out)
);
assign out = _join_out;
endmodule

module Mux4xOutBits6 (
    input [5:0] I0,
    input [5:0] I1,
    input [5:0] I2,
    input [5:0] I3,
    input [1:0] S,
    output [5:0] O
);
wire [5:0] coreir_commonlib_mux4x6_inst0_out;
commonlib_muxn__N4__width6 coreir_commonlib_mux4x6_inst0 (
    .in_data({I3,I2,I1,I0}),
    .in_sel(S),
    .out(coreir_commonlib_mux4x6_inst0_out)
);
assign O = coreir_commonlib_mux4x6_inst0_out;
endmodule

module TestSlice (
    input [9:0] I,
    input [1:0] x,
    output [5:0] O
);
wire [5:0] Mux4xOutBits6_inst0_O;
Mux4xOutBits6 Mux4xOutBits6_inst0 (
    .I0(I[5:0]),
    .I1(I[6:1]),
    .I2(I[7:2]),
    .I3(I[8:3]),
    .S(x),
    .O(Mux4xOutBits6_inst0_O)
);
assign O = Mux4xOutBits6_inst0_O;
endmodule

