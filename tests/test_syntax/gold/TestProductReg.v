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

module commonlib_muxn__N2__width1 (
    input [0:0] in_data_0,
    input [0:0] in_data_1,
    input [0:0] in_sel,
    output [0:0] out
);
wire [0:0] _join_out;
coreir_mux #(
    .width(1)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xOutSInt8 (
    input [7:0] I0,
    input [7:0] I1,
    input S,
    output [7:0] O
);
wire [7:0] coreir_commonlib_mux2x8_inst0_out;
commonlib_muxn__N2__width8 coreir_commonlib_mux2x8_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_sel(S),
    .out(coreir_commonlib_mux2x8_inst0_out)
);
assign O = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Mux2xOutBit (
    input I0,
    input I1,
    input S,
    output O
);
wire [0:0] coreir_commonlib_mux2x1_inst0_out;
commonlib_muxn__N2__width1 coreir_commonlib_mux2x1_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_sel(S),
    .out(coreir_commonlib_mux2x1_inst0_out)
);
assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module Mux2xTuplea0_OutBit_a1_OutSInt8 (
    input I0_a0,
    input [7:0] I0_a1,
    input I1_a0,
    input [7:0] I1_a1,
    output O_a0,
    output [7:0] O_a1,
    input S
);
wire Mux2xOutBit_inst0_O;
wire [7:0] Mux2xOutSInt8_inst0_O;
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(I0_a0),
    .I1(I1_a0),
    .S(S),
    .O(Mux2xOutBit_inst0_O)
);
Mux2xOutSInt8 Mux2xOutSInt8_inst0 (
    .I0(I0_a1),
    .I1(I1_a1),
    .S(S),
    .O(Mux2xOutSInt8_inst0_O)
);
assign O_a0 = Mux2xOutBit_inst0_O;
assign O_a1 = Mux2xOutSInt8_inst0_O;
endmodule

module TestProductReg_comb (
    output O0_a0,
    output [7:0] O0_a1,
    output O1_a0,
    output [7:0] O1_a1,
    input a_a0,
    input [7:0] a_a1,
    input b,
    input self_a_O_a0,
    input [7:0] self_a_O_a1
);
wire Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a0;
wire [7:0] Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a1;
Mux2xTuplea0_OutBit_a1_OutSInt8 Mux2xTuplea0_OutBit_a1_OutSInt8_inst0 (
    .I0_a0(self_a_O_a0),
    .I0_a1(self_a_O_a1),
    .I1_a0(a_a0),
    .I1_a1(a_a1),
    .O_a0(Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a0),
    .O_a1(Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a1),
    .S(b)
);
assign O0_a0 = Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a0;
assign O0_a1 = Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a1;
assign O1_a0 = Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a0;
assign O1_a1 = Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a1;
endmodule

module DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue (
    input I,
    output O,
    input CLK,
    input ASYNCRESET
);
wire [0:0] reg_PR_inst0_out;
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1'h1),
    .width(1)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(I),
    .out(reg_PR_inst0_out)
);
assign O = reg_PR_inst0_out[0];
endmodule

module TestProductReg (
    input ASYNCRESET,
    input CLK,
    output O_a0,
    output [7:0] O_a1,
    input a_a0,
    input [7:0] a_a1,
    input b
);
wire DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O;
wire TestProductReg_comb_inst0_O0_a0;
wire [7:0] TestProductReg_comb_inst0_O0_a1;
wire TestProductReg_comb_inst0_O1_a0;
wire [7:0] TestProductReg_comb_inst0_O1_a1;
wire [7:0] reg_PR_inst0_out;
DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0 (
    .I(TestProductReg_comb_inst0_O0_a0),
    .O(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET)
);
TestProductReg_comb TestProductReg_comb_inst0 (
    .O0_a0(TestProductReg_comb_inst0_O0_a0),
    .O0_a1(TestProductReg_comb_inst0_O0_a1),
    .O1_a0(TestProductReg_comb_inst0_O1_a0),
    .O1_a1(TestProductReg_comb_inst0_O1_a1),
    .a_a0(a_a0),
    .a_a1(a_a1),
    .b(b),
    .self_a_O_a0(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O),
    .self_a_O_a1(reg_PR_inst0_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(8'h02),
    .width(8)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(TestProductReg_comb_inst0_O0_a1),
    .out(reg_PR_inst0_out)
);
assign O_a0 = TestProductReg_comb_inst0_O1_a0;
assign O_a1 = TestProductReg_comb_inst0_O1_a1;
endmodule

