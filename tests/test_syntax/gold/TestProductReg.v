module mantle_wire__typeBitIn9 (
    output [8:0] in,
    input [8:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBitIn8 (
    output [7:0] in,
    input [7:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit9 (
    input [8:0] in,
    output [8:0] out
);
assign out = in;
endmodule

module mantle_wire__typeBit8 (
    input [7:0] in,
    output [7:0] out
);
assign out = in;
endmodule

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

module commonlib_muxn__N2__width9 (
    input [8:0] in_data [1:0],
    input [0:0] in_sel,
    output [8:0] out
);
wire [8:0] _join_in0;
wire [8:0] _join_in1;
wire _join_sel;
wire [8:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(9)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
    .out(_join_out)
);
assign out = _join_out;
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
wire [8:0] _$_U2_in;
wire [8:0] _$_U2_out;
wire [8:0] _$_U3_in;
wire [8:0] _$_U3_out;
wire [8:0] _$_U4_in;
wire [8:0] _$_U4_out;
wire [7:0] _$_U6_in;
wire [7:0] _$_U6_out;
wire [7:0] _$_U7_in;
wire [7:0] _$_U7_out;
wire [7:0] _$_U8_in;
wire [7:0] _$_U8_out;
wire [8:0] coreir_commonlib_mux2x9_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x9_inst0_in_sel;
wire [8:0] coreir_commonlib_mux2x9_inst0_out;
assign _$_U2_out = {_$_U6_out[7:0],I0_a0};
mantle_wire__typeBitIn9 _$_U2 (
    .in(_$_U2_in),
    .out(_$_U2_out)
);
assign _$_U3_out = {_$_U7_out[7:0],I1_a0};
mantle_wire__typeBitIn9 _$_U3 (
    .in(_$_U3_in),
    .out(_$_U3_out)
);
assign _$_U4_in = coreir_commonlib_mux2x9_inst0_out;
mantle_wire__typeBit9 _$_U4 (
    .in(_$_U4_in),
    .out(_$_U4_out)
);
assign _$_U6_in = I0_a1;
mantle_wire__typeBit8 _$_U6 (
    .in(_$_U6_in),
    .out(_$_U6_out)
);
assign _$_U7_in = I1_a1;
mantle_wire__typeBit8 _$_U7 (
    .in(_$_U7_in),
    .out(_$_U7_out)
);
assign _$_U8_out = _$_U4_out[8:1];
mantle_wire__typeBitIn8 _$_U8 (
    .in(_$_U8_in),
    .out(_$_U8_out)
);
assign coreir_commonlib_mux2x9_inst0_in_data[1] = _$_U3_in;
assign coreir_commonlib_mux2x9_inst0_in_data[0] = _$_U2_in;
assign coreir_commonlib_mux2x9_inst0_in_sel[0] = S;
commonlib_muxn__N2__width9 coreir_commonlib_mux2x9_inst0 (
    .in_data(coreir_commonlib_mux2x9_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x9_inst0_in_sel),
    .out(coreir_commonlib_mux2x9_inst0_out)
);
assign O_a0 = _$_U4_out[0];
assign O_a1 = _$_U8_in;
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
wire Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I0_a0;
wire [7:0] Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I0_a1;
wire Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I1_a0;
wire [7:0] Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I1_a1;
wire Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a0;
wire [7:0] Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a1;
wire Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_S;
assign Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I0_a0 = self_a_O_a0;
assign Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I0_a1 = self_a_O_a1;
assign Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I1_a0 = a_a0;
assign Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I1_a1 = a_a1;
assign Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_S = b;
Mux2xTuplea0_OutBit_a1_OutSInt8 Mux2xTuplea0_OutBit_a1_OutSInt8_inst0 (
    .I0_a0(Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I0_a0),
    .I0_a1(Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I0_a1),
    .I1_a0(Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I1_a0),
    .I1_a1(Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_I1_a1),
    .O_a0(Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a0),
    .O_a1(Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_O_a1),
    .S(Mux2xTuplea0_OutBit_a1_OutSInt8_inst0_S)
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
wire reg_PR_inst0_clk;
wire reg_PR_inst0_arst;
wire [0:0] reg_PR_inst0_in;
wire [0:0] reg_PR_inst0_out;
assign reg_PR_inst0_clk = CLK;
assign reg_PR_inst0_arst = ASYNCRESET;
assign reg_PR_inst0_in[0] = I;
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1'h1),
    .width(1)
) reg_PR_inst0 (
    .clk(reg_PR_inst0_clk),
    .arst(reg_PR_inst0_arst),
    .in(reg_PR_inst0_in),
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
wire DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_I;
wire DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O;
wire DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_CLK;
wire DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_ASYNCRESET;
wire TestProductReg_comb_inst0_O0_a0;
wire [7:0] TestProductReg_comb_inst0_O0_a1;
wire TestProductReg_comb_inst0_O1_a0;
wire [7:0] TestProductReg_comb_inst0_O1_a1;
wire TestProductReg_comb_inst0_a_a0;
wire [7:0] TestProductReg_comb_inst0_a_a1;
wire TestProductReg_comb_inst0_b;
wire TestProductReg_comb_inst0_self_a_O_a0;
wire [7:0] TestProductReg_comb_inst0_self_a_O_a1;
wire reg_PR_inst0_clk;
wire reg_PR_inst0_arst;
wire [7:0] reg_PR_inst0_in;
wire [7:0] reg_PR_inst0_out;
assign DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_I = TestProductReg_comb_inst0_O0_a0;
assign DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_CLK = CLK;
assign DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_ASYNCRESET = ASYNCRESET;
DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0 (
    .I(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_I),
    .O(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O),
    .CLK(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_CLK),
    .ASYNCRESET(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_ASYNCRESET)
);
assign TestProductReg_comb_inst0_a_a0 = a_a0;
assign TestProductReg_comb_inst0_a_a1 = a_a1;
assign TestProductReg_comb_inst0_b = b;
assign TestProductReg_comb_inst0_self_a_O_a0 = DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O;
assign TestProductReg_comb_inst0_self_a_O_a1 = reg_PR_inst0_out;
TestProductReg_comb TestProductReg_comb_inst0 (
    .O0_a0(TestProductReg_comb_inst0_O0_a0),
    .O0_a1(TestProductReg_comb_inst0_O0_a1),
    .O1_a0(TestProductReg_comb_inst0_O1_a0),
    .O1_a1(TestProductReg_comb_inst0_O1_a1),
    .a_a0(TestProductReg_comb_inst0_a_a0),
    .a_a1(TestProductReg_comb_inst0_a_a1),
    .b(TestProductReg_comb_inst0_b),
    .self_a_O_a0(TestProductReg_comb_inst0_self_a_O_a0),
    .self_a_O_a1(TestProductReg_comb_inst0_self_a_O_a1)
);
assign reg_PR_inst0_clk = CLK;
assign reg_PR_inst0_arst = ASYNCRESET;
assign reg_PR_inst0_in = TestProductReg_comb_inst0_O0_a1;
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(8'h02),
    .width(8)
) reg_PR_inst0 (
    .clk(reg_PR_inst0_clk),
    .arst(reg_PR_inst0_arst),
    .in(reg_PR_inst0_in),
    .out(reg_PR_inst0_out)
);
assign O_a0 = TestProductReg_comb_inst0_O1_a0;
assign O_a1 = TestProductReg_comb_inst0_O1_a1;
endmodule

