module mantle_wire__typeBitIn8 (
    output [7:0] in,
    input [7:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBitIn4 (
    output [3:0] in,
    input [3:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBitIn14 (
    output [13:0] in,
    input [13:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit8 (
    input [7:0] in,
    output [7:0] out
);
assign out = in;
endmodule

module mantle_wire__typeBit4 (
    input [3:0] in,
    output [3:0] out
);
assign out = in;
endmodule

module mantle_wire__typeBit14 (
    input [13:0] in,
    output [13:0] out
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

module commonlib_muxn__N2__width14 (
    input [13:0] in_data [1:0],
    input [0:0] in_sel,
    output [13:0] out
);
wire [13:0] _join_out;
coreir_mux #(
    .width(14)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8 (
    input I0_a0,
    input [3:0] I0_a1_c0,
    input I0_a1_c1,
    input [7:0] I0_a2,
    input I1_a0,
    input [3:0] I1_a1_c0,
    input I1_a1_c1,
    input [7:0] I1_a2,
    output O_a0,
    output [3:0] O_a1_c0,
    output O_a1_c1,
    output [7:0] O_a2,
    input S
);
wire [13:0] coreir_commonlib_mux2x14_inst0_out_unq1;
wire [13:0] coreir_commonlib_mux2x14_inst0_in_data_0_in;
wire [13:0] coreir_commonlib_mux2x14_inst0_in_data_1_in;
wire [13:0] coreir_commonlib_mux2x14_inst0_out_out;
wire [3:0] self_I0_a1_c0_out;
wire [7:0] self_I0_a2_out;
wire [3:0] self_I1_a1_c0_out;
wire [7:0] self_I1_a2_out;
wire [3:0] self_O_a1_c0_in;
wire [7:0] self_O_a2_in;
wire [13:0] coreir_commonlib_mux2x14_inst0_in_data [1:0];
assign coreir_commonlib_mux2x14_inst0_in_data[1] = coreir_commonlib_mux2x14_inst0_in_data_1_in;
assign coreir_commonlib_mux2x14_inst0_in_data[0] = coreir_commonlib_mux2x14_inst0_in_data_0_in;
commonlib_muxn__N2__width14 coreir_commonlib_mux2x14_inst0 (
    .in_data(coreir_commonlib_mux2x14_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x14_inst0_out_unq1)
);
wire [13:0] coreir_commonlib_mux2x14_inst0_in_data_0_out;
assign coreir_commonlib_mux2x14_inst0_in_data_0_out = {self_I0_a2_out[7:0],I0_a1_c1,self_I0_a1_c0_out[3:0],I0_a0};
mantle_wire__typeBitIn14 coreir_commonlib_mux2x14_inst0_in_data_0 (
    .in(coreir_commonlib_mux2x14_inst0_in_data_0_in),
    .out(coreir_commonlib_mux2x14_inst0_in_data_0_out)
);
wire [13:0] coreir_commonlib_mux2x14_inst0_in_data_1_out;
assign coreir_commonlib_mux2x14_inst0_in_data_1_out = {self_I1_a2_out[7:0],I1_a1_c1,self_I1_a1_c0_out[3:0],I1_a0};
mantle_wire__typeBitIn14 coreir_commonlib_mux2x14_inst0_in_data_1 (
    .in(coreir_commonlib_mux2x14_inst0_in_data_1_in),
    .out(coreir_commonlib_mux2x14_inst0_in_data_1_out)
);
mantle_wire__typeBit14 coreir_commonlib_mux2x14_inst0_out (
    .in(coreir_commonlib_mux2x14_inst0_out_unq1),
    .out(coreir_commonlib_mux2x14_inst0_out_out)
);
mantle_wire__typeBit4 self_I0_a1_c0 (
    .in(I0_a1_c0),
    .out(self_I0_a1_c0_out)
);
mantle_wire__typeBit8 self_I0_a2 (
    .in(I0_a2),
    .out(self_I0_a2_out)
);
mantle_wire__typeBit4 self_I1_a1_c0 (
    .in(I1_a1_c0),
    .out(self_I1_a1_c0_out)
);
mantle_wire__typeBit8 self_I1_a2 (
    .in(I1_a2),
    .out(self_I1_a2_out)
);
mantle_wire__typeBitIn4 self_O_a1_c0 (
    .in(self_O_a1_c0_in),
    .out(coreir_commonlib_mux2x14_inst0_out_out[4:1])
);
mantle_wire__typeBitIn8 self_O_a2 (
    .in(self_O_a2_in),
    .out(coreir_commonlib_mux2x14_inst0_out_out[13:6])
);
assign O_a0 = coreir_commonlib_mux2x14_inst0_out_out[0];
assign O_a1_c0 = self_O_a1_c0_in;
assign O_a1_c1 = coreir_commonlib_mux2x14_inst0_out_out[5];
assign O_a2 = self_O_a2_in;
endmodule

module TestNestedProductReg_comb (
    output O0_a0,
    output [3:0] O0_a1_c0,
    output O0_a1_c1,
    output [7:0] O0_a2,
    output O1_a0,
    output [3:0] O1_a1_c0,
    output O1_a1_c1,
    output [7:0] O1_a2,
    input a_a0,
    input [3:0] a_a1_c0,
    input a_a1_c1,
    input [7:0] a_a2,
    input b,
    input self_a_O_a0,
    input [3:0] self_a_O_a1_c0,
    input self_a_O_a1_c1,
    input [7:0] self_a_O_a2
);
wire Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a0;
wire [3:0] Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a1_c0;
wire Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a1_c1;
wire [7:0] Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a2;
Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8 Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0 (
    .I0_a0(self_a_O_a0),
    .I0_a1_c0(self_a_O_a1_c0),
    .I0_a1_c1(self_a_O_a1_c1),
    .I0_a2(self_a_O_a2),
    .I1_a0(a_a0),
    .I1_a1_c0(a_a1_c0),
    .I1_a1_c1(a_a1_c1),
    .I1_a2(a_a2),
    .O_a0(Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a0),
    .O_a1_c0(Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a1_c0),
    .O_a1_c1(Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a1_c1),
    .O_a2(Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a2),
    .S(b)
);
assign O0_a0 = Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a0;
assign O0_a1_c0 = Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a1_c0;
assign O0_a1_c1 = Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a1_c1;
assign O0_a2 = Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a2;
assign O1_a0 = Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a0;
assign O1_a1_c0 = Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a1_c0;
assign O1_a1_c1 = Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a1_c1;
assign O1_a2 = Mux2xTuplea0_Bit_a1_Tuplec0_UInt4_c1_Bit_a2_SInt8_inst0_O_a2;
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

module DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue (
    input I,
    output O,
    input CLK,
    input ASYNCRESET
);
wire [0:0] reg_PR_inst0_out;
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(I),
    .out(reg_PR_inst0_out)
);
assign O = reg_PR_inst0_out[0];
endmodule

module TestNestedProductReg (
    input ASYNCRESET,
    input CLK,
    output O_a0,
    output [3:0] O_a1_c0,
    output O_a1_c1,
    output [7:0] O_a2,
    input a_a0,
    input [3:0] a_a1_c0,
    input a_a1_c1,
    input [7:0] a_a2,
    input b
);
wire DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O;
wire DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O;
wire TestNestedProductReg_comb_inst0_O0_a0;
wire [3:0] TestNestedProductReg_comb_inst0_O0_a1_c0;
wire TestNestedProductReg_comb_inst0_O0_a1_c1;
wire [7:0] TestNestedProductReg_comb_inst0_O0_a2;
wire TestNestedProductReg_comb_inst0_O1_a0;
wire [3:0] TestNestedProductReg_comb_inst0_O1_a1_c0;
wire TestNestedProductReg_comb_inst0_O1_a1_c1;
wire [7:0] TestNestedProductReg_comb_inst0_O1_a2;
wire [3:0] reg_PR_inst0_out;
wire [7:0] reg_PR_inst1_out;
DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0 (
    .I(TestNestedProductReg_comb_inst0_O0_a1_c1),
    .O(DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET)
);
DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0 (
    .I(TestNestedProductReg_comb_inst0_O0_a0),
    .O(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET)
);
TestNestedProductReg_comb TestNestedProductReg_comb_inst0 (
    .O0_a0(TestNestedProductReg_comb_inst0_O0_a0),
    .O0_a1_c0(TestNestedProductReg_comb_inst0_O0_a1_c0),
    .O0_a1_c1(TestNestedProductReg_comb_inst0_O0_a1_c1),
    .O0_a2(TestNestedProductReg_comb_inst0_O0_a2),
    .O1_a0(TestNestedProductReg_comb_inst0_O1_a0),
    .O1_a1_c0(TestNestedProductReg_comb_inst0_O1_a1_c0),
    .O1_a1_c1(TestNestedProductReg_comb_inst0_O1_a1_c1),
    .O1_a2(TestNestedProductReg_comb_inst0_O1_a2),
    .a_a0(a_a0),
    .a_a1_c0(a_a1_c0),
    .a_a1_c1(a_a1_c1),
    .a_a2(a_a2),
    .b(b),
    .self_a_O_a0(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O),
    .self_a_O_a1_c0(reg_PR_inst0_out),
    .self_a_O_a1_c1(DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O),
    .self_a_O_a2(reg_PR_inst1_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(4'h3),
    .width(4)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(TestNestedProductReg_comb_inst0_O0_a1_c0),
    .out(reg_PR_inst0_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(8'h02),
    .width(8)
) reg_PR_inst1 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(TestNestedProductReg_comb_inst0_O0_a2),
    .out(reg_PR_inst1_out)
);
assign O_a0 = TestNestedProductReg_comb_inst0_O1_a0;
assign O_a1_c0 = TestNestedProductReg_comb_inst0_O1_a1_c0;
assign O_a1_c1 = TestNestedProductReg_comb_inst0_O1_a1_c1;
assign O_a2 = TestNestedProductReg_comb_inst0_O1_a2;
endmodule

