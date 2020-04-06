module coreir_uge #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 >= in1;
endmodule

module coreir_reg #(
    parameter width = 1,
    parameter clk_posedge = 1,
    parameter init = 1
) (
    input clk,
    input [width-1:0] in,
    output [width-1:0] out
);
  reg [width-1:0] outReg=init;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk) begin
    outReg <= in;
  end
  assign out = outReg;
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

module coreir_eq #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 == in1;
endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module commonlib_muxn__N2__width4 (
    input [3:0] in_data_0,
    input [3:0] in_data_1,
    input [0:0] in_sel,
    output [3:0] out
);
wire [3:0] _join_out;
coreir_mux #(
    .width(4)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xOutBits4 (
    input [3:0] I0,
    input [3:0] I1,
    input S,
    output [3:0] O
);
wire [3:0] coreir_commonlib_mux2x4_inst0_out;
commonlib_muxn__N2__width4 coreir_commonlib_mux2x4_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_sel(S),
    .out(coreir_commonlib_mux2x4_inst0_out)
);
assign O = coreir_commonlib_mux2x4_inst0_out;
endmodule

module Register_has_ce_True_has_reset_False_has_async_reset_False_has_async_resetn_False_type_Bits_n_4 (
    input [3:0] I,
    output [3:0] O,
    input CLK,
    input CE
);
wire [3:0] enable_mux_O;
wire [3:0] value_out;
Mux2xOutBits4 enable_mux (
    .I0(value_out),
    .I1(I),
    .S(CE),
    .O(enable_mux_O)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) value (
    .clk(CLK),
    .in(enable_mux_O),
    .out(value_out)
);
assign O = value_out;
endmodule

module Basic (
    input [2:0] opcode,
    input [3:0] I,
    output [3:0] out,
    input CLK,
    input CE
);
wire [3:0] Register_has_ce_True_has_reset_False_has_async_reset_False_has_async_resetn_False_type_Bits_n_4_inst0_O;
wire [3:0] Register_has_ce_True_has_reset_False_has_async_reset_False_has_async_resetn_False_type_Bits_n_4_inst1_O;
wire [2:0] const_2_3_out;
wire [2:0] const_3_3_out;
wire magma_Bits_3_eq_inst0_out;
wire magma_Bits_3_uge_inst0_out;
Register_has_ce_True_has_reset_False_has_async_reset_False_has_async_resetn_False_type_Bits_n_4 Register_has_ce_True_has_reset_False_has_async_reset_False_has_async_resetn_False_type_Bits_n_4_inst0 (
    .I(I),
    .O(Register_has_ce_True_has_reset_False_has_async_reset_False_has_async_resetn_False_type_Bits_n_4_inst0_O),
    .CLK(CLK),
    .CE(magma_Bits_3_uge_inst0_out)
);
Register_has_ce_True_has_reset_False_has_async_reset_False_has_async_resetn_False_type_Bits_n_4 Register_has_ce_True_has_reset_False_has_async_reset_False_has_async_resetn_False_type_Bits_n_4_inst1 (
    .I(Register_has_ce_True_has_reset_False_has_async_reset_False_has_async_resetn_False_type_Bits_n_4_inst0_O),
    .O(Register_has_ce_True_has_reset_False_has_async_reset_False_has_async_resetn_False_type_Bits_n_4_inst1_O),
    .CLK(CLK),
    .CE(magma_Bits_3_eq_inst0_out)
);
coreir_const #(
    .value(3'h2),
    .width(3)
) const_2_3 (
    .out(const_2_3_out)
);
coreir_const #(
    .value(3'h3),
    .width(3)
) const_3_3 (
    .out(const_3_3_out)
);
coreir_eq #(
    .width(3)
) magma_Bits_3_eq_inst0 (
    .in0(opcode),
    .in1(const_3_3_out),
    .out(magma_Bits_3_eq_inst0_out)
);
coreir_uge #(
    .width(3)
) magma_Bits_3_uge_inst0 (
    .in0(opcode),
    .in1(const_2_3_out),
    .out(magma_Bits_3_uge_inst0_out)
);
assign out = Register_has_ce_True_has_reset_False_has_async_reset_False_has_async_resetn_False_type_Bits_n_4_inst1_O;
endmodule

