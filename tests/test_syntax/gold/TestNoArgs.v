module coreir_reg_arst #(
    parameter width = 1,
    parameter arst_posedge = 1,
    parameter clk_posedge = 1,
    parameter init = 1
) (
    input clk,
    input arst,
    input [width-1:0] in,
    output [width-1:0] out
);
  reg [width-1:0] outReg;
  wire real_rst;
  assign real_rst = arst_posedge ? arst : ~arst;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk, posedge real_rst) begin
    if (real_rst) outReg <= init;
    else outReg <= in;
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

module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module commonlib_muxn__N2__width3 (
    input [2:0] in_data [1:0],
    input [0:0] in_sel,
    output [2:0] out
);
wire [2:0] _join_in0;
wire [2:0] _join_in1;
wire _join_sel;
wire [2:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(3)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xOutUInt3 (
    input [2:0] I0,
    input [2:0] I1,
    input S,
    output [2:0] O
);
wire [2:0] coreir_commonlib_mux2x3_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x3_inst0_in_sel;
wire [2:0] coreir_commonlib_mux2x3_inst0_out;
assign coreir_commonlib_mux2x3_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x3_inst0_in_data[0] = I0;
assign coreir_commonlib_mux2x3_inst0_in_sel[0] = S;
commonlib_muxn__N2__width3 coreir_commonlib_mux2x3_inst0 (
    .in_data(coreir_commonlib_mux2x3_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x3_inst0_in_sel),
    .out(coreir_commonlib_mux2x3_inst0_out)
);
assign O = coreir_commonlib_mux2x3_inst0_out;
endmodule

module TestNoArgs_comb (
    input [1:0] self_x_O,
    input [2:0] self_y_O,
    output [1:0] O0,
    output [2:0] O1,
    output [2:0] O2
);
wire [2:0] Mux2xOutUInt3_inst0_I0;
wire [2:0] Mux2xOutUInt3_inst0_I1;
wire Mux2xOutUInt3_inst0_S;
wire [2:0] Mux2xOutUInt3_inst0_O;
wire [1:0] const_1_2_out;
wire [2:0] const_1_3_out;
wire [1:0] const_3_2_out;
wire [1:0] magma_Bits_2_add_inst0_in0;
wire [1:0] magma_Bits_2_add_inst0_in1;
wire [1:0] magma_Bits_2_add_inst0_out;
wire [1:0] magma_Bits_2_eq_inst0_in0;
wire [1:0] magma_Bits_2_eq_inst0_in1;
wire magma_Bits_2_eq_inst0_out;
wire [2:0] magma_Bits_3_add_inst0_in0;
wire [2:0] magma_Bits_3_add_inst0_in1;
wire [2:0] magma_Bits_3_add_inst0_out;
assign Mux2xOutUInt3_inst0_I0 = self_y_O;
assign Mux2xOutUInt3_inst0_I1 = magma_Bits_3_add_inst0_out;
assign Mux2xOutUInt3_inst0_S = magma_Bits_2_eq_inst0_out;
Mux2xOutUInt3 Mux2xOutUInt3_inst0 (
    .I0(Mux2xOutUInt3_inst0_I0),
    .I1(Mux2xOutUInt3_inst0_I1),
    .S(Mux2xOutUInt3_inst0_S),
    .O(Mux2xOutUInt3_inst0_O)
);
coreir_const #(
    .value(2'h1),
    .width(2)
) const_1_2 (
    .out(const_1_2_out)
);
coreir_const #(
    .value(3'h1),
    .width(3)
) const_1_3 (
    .out(const_1_3_out)
);
coreir_const #(
    .value(2'h3),
    .width(2)
) const_3_2 (
    .out(const_3_2_out)
);
assign magma_Bits_2_add_inst0_in0 = self_x_O;
assign magma_Bits_2_add_inst0_in1 = const_1_2_out;
coreir_add #(
    .width(2)
) magma_Bits_2_add_inst0 (
    .in0(magma_Bits_2_add_inst0_in0),
    .in1(magma_Bits_2_add_inst0_in1),
    .out(magma_Bits_2_add_inst0_out)
);
assign magma_Bits_2_eq_inst0_in0 = magma_Bits_2_add_inst0_out;
assign magma_Bits_2_eq_inst0_in1 = const_3_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst0 (
    .in0(magma_Bits_2_eq_inst0_in0),
    .in1(magma_Bits_2_eq_inst0_in1),
    .out(magma_Bits_2_eq_inst0_out)
);
assign magma_Bits_3_add_inst0_in0 = self_y_O;
assign magma_Bits_3_add_inst0_in1 = const_1_3_out;
coreir_add #(
    .width(3)
) magma_Bits_3_add_inst0 (
    .in0(magma_Bits_3_add_inst0_in0),
    .in1(magma_Bits_3_add_inst0_in1),
    .out(magma_Bits_3_add_inst0_out)
);
assign O0 = magma_Bits_2_add_inst0_out;
assign O1 = Mux2xOutUInt3_inst0_O;
assign O2 = Mux2xOutUInt3_inst0_O;
endmodule

module TestNoArgs (
    input CLK,
    input ASYNCRESET,
    output [2:0] O
);
wire [1:0] TestNoArgs_comb_inst0_self_x_O;
wire [2:0] TestNoArgs_comb_inst0_self_y_O;
wire [1:0] TestNoArgs_comb_inst0_O0;
wire [2:0] TestNoArgs_comb_inst0_O1;
wire [2:0] TestNoArgs_comb_inst0_O2;
wire reg_PR_inst0_clk;
wire reg_PR_inst0_arst;
wire [1:0] reg_PR_inst0_in;
wire [1:0] reg_PR_inst0_out;
wire reg_PR_inst1_clk;
wire reg_PR_inst1_arst;
wire [2:0] reg_PR_inst1_in;
wire [2:0] reg_PR_inst1_out;
assign TestNoArgs_comb_inst0_self_x_O = reg_PR_inst0_out;
assign TestNoArgs_comb_inst0_self_y_O = reg_PR_inst1_out;
TestNoArgs_comb TestNoArgs_comb_inst0 (
    .self_x_O(TestNoArgs_comb_inst0_self_x_O),
    .self_y_O(TestNoArgs_comb_inst0_self_y_O),
    .O0(TestNoArgs_comb_inst0_O0),
    .O1(TestNoArgs_comb_inst0_O1),
    .O2(TestNoArgs_comb_inst0_O2)
);
assign reg_PR_inst0_clk = CLK;
assign reg_PR_inst0_arst = ASYNCRESET;
assign reg_PR_inst0_in = TestNoArgs_comb_inst0_O0;
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(2'h0),
    .width(2)
) reg_PR_inst0 (
    .clk(reg_PR_inst0_clk),
    .arst(reg_PR_inst0_arst),
    .in(reg_PR_inst0_in),
    .out(reg_PR_inst0_out)
);
assign reg_PR_inst1_clk = CLK;
assign reg_PR_inst1_arst = ASYNCRESET;
assign reg_PR_inst1_in = TestNoArgs_comb_inst0_O1;
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_PR_inst1 (
    .clk(reg_PR_inst1_clk),
    .arst(reg_PR_inst1_arst),
    .in(reg_PR_inst1_in),
    .out(reg_PR_inst1_out)
);
assign O = TestNoArgs_comb_inst0_O2;
endmodule

