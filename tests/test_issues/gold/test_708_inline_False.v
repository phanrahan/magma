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

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module commonlib_muxn__N2__width8 (
    input [7:0] in_data_0,
    input [7:0] in_data_1,
    input [0:0] in_sel,
    output [7:0] out
);
wire [7:0] _join_out;
coreir_mux #(
    .width(8)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xTuplex_UInt8 (
    input [7:0] I0_x,
    input [7:0] I1_x,
    output [7:0] O_x,
    input S
);
wire [7:0] coreir_commonlib_mux2x8_inst0_out;
commonlib_muxn__N2__width8 coreir_commonlib_mux2x8_inst0 (
    .in_data_0(I0_x),
    .in_data_1(I1_x),
    .in_sel(S),
    .out(coreir_commonlib_mux2x8_inst0_out)
);
assign O_x = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Test (
    input CLK,
    output [7:0] O_a_x,
    input c
);
wire [7:0] Mux2xTuplex_UInt8_inst0_O_x;
wire [7:0] const_0_8_out;
wire [7:0] const_1_8_out;
wire [7:0] magma_UInt_8_add_inst0_out;
Mux2xTuplex_UInt8 Mux2xTuplex_UInt8_inst0 (
    .I0_x(const_0_8_out),
    .I1_x(magma_UInt_8_add_inst0_out),
    .O_x(Mux2xTuplex_UInt8_inst0_O_x),
    .S(c)
);
coreir_const #(
    .value(8'h00),
    .width(8)
) const_0_8 (
    .out(const_0_8_out)
);
coreir_const #(
    .value(8'h01),
    .width(8)
) const_1_8 (
    .out(const_1_8_out)
);
coreir_add #(
    .width(8)
) magma_UInt_8_add_inst0 (
    .in0(const_0_8_out),
    .in1(const_1_8_out),
    .out(magma_UInt_8_add_inst0_out)
);
assign O_a_x = Mux2xTuplex_UInt8_inst0_O_x;
endmodule

