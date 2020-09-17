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
wire [2:0] _join_out;
coreir_mux #(
    .width(3)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xUInt3 (
    input [2:0] I0,
    input [2:0] I1,
    input S,
    output [2:0] O
);
wire [2:0] coreir_commonlib_mux2x3_inst0_out;
wire [2:0] coreir_commonlib_mux2x3_inst0_in_data [1:0];
assign coreir_commonlib_mux2x3_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x3_inst0_in_data[0] = I0;
commonlib_muxn__N2__width3 coreir_commonlib_mux2x3_inst0 (
    .in_data(coreir_commonlib_mux2x3_inst0_in_data),
    .in_sel(S),
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
wire [2:0] Mux2xUInt3_inst0_O;
wire [1:0] const_1_2_out;
wire [2:0] const_1_3_out;
wire [1:0] const_3_2_out;
wire [1:0] magma_Bits_2_add_inst0_out;
wire magma_Bits_2_eq_inst0_out;
wire [2:0] magma_Bits_3_add_inst0_out;
Mux2xUInt3 Mux2xUInt3_inst0 (
    .I0(self_y_O),
    .I1(magma_Bits_3_add_inst0_out),
    .S(magma_Bits_2_eq_inst0_out),
    .O(Mux2xUInt3_inst0_O)
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
coreir_add #(
    .width(2)
) magma_Bits_2_add_inst0 (
    .in0(self_x_O),
    .in1(const_1_2_out),
    .out(magma_Bits_2_add_inst0_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst0 (
    .in0(magma_Bits_2_add_inst0_out),
    .in1(const_3_2_out),
    .out(magma_Bits_2_eq_inst0_out)
);
coreir_add #(
    .width(3)
) magma_Bits_3_add_inst0 (
    .in0(self_y_O),
    .in1(const_1_3_out),
    .out(magma_Bits_3_add_inst0_out)
);
assign O0 = magma_Bits_2_add_inst0_out;
assign O1 = Mux2xUInt3_inst0_O;
assign O2 = Mux2xUInt3_inst0_O;
endmodule

module TestNoArgs (
    input CLK,
    input ASYNCRESET,
    output [2:0] O
);
wire [1:0] TestNoArgs_comb_inst0_O0;
wire [2:0] TestNoArgs_comb_inst0_O1;
wire [2:0] TestNoArgs_comb_inst0_O2;
wire [1:0] reg_PR_inst0_out;
wire [2:0] reg_PR_inst1_out;
TestNoArgs_comb TestNoArgs_comb_inst0 (
    .self_x_O(reg_PR_inst0_out),
    .self_y_O(reg_PR_inst1_out),
    .O0(TestNoArgs_comb_inst0_O0),
    .O1(TestNoArgs_comb_inst0_O1),
    .O2(TestNoArgs_comb_inst0_O2)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(2'h0),
    .width(2)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(TestNoArgs_comb_inst0_O0),
    .out(reg_PR_inst0_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_PR_inst1 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(TestNoArgs_comb_inst0_O1),
    .out(reg_PR_inst1_out)
);
assign O = TestNoArgs_comb_inst0_O2;
endmodule

