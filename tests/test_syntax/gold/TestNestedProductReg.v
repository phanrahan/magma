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
wire [13:0] _join_in0;
wire [13:0] _join_in1;
wire _join_sel;
wire [13:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(14)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8 (
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
wire [3:0] _$_U10_in;
wire [3:0] _$_U10_out;
wire [7:0] _$_U11_in;
wire [7:0] _$_U11_out;
wire [13:0] _$_U2_in;
wire [13:0] _$_U2_out;
wire [13:0] _$_U3_in;
wire [13:0] _$_U3_out;
wire [13:0] _$_U4_in;
wire [13:0] _$_U4_out;
wire [3:0] _$_U6_in;
wire [3:0] _$_U6_out;
wire [7:0] _$_U7_in;
wire [7:0] _$_U7_out;
wire [3:0] _$_U8_in;
wire [3:0] _$_U8_out;
wire [7:0] _$_U9_in;
wire [7:0] _$_U9_out;
wire [13:0] coreir_commonlib_mux2x14_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x14_inst0_in_sel;
wire [13:0] coreir_commonlib_mux2x14_inst0_out;
assign _$_U10_out = _$_U4_out[4:1];
mantle_wire__typeBitIn4 _$_U10 (
    .in(_$_U10_in),
    .out(_$_U10_out)
);
assign _$_U11_out = _$_U4_out[13:6];
mantle_wire__typeBitIn8 _$_U11 (
    .in(_$_U11_in),
    .out(_$_U11_out)
);
assign _$_U2_out = {_$_U7_out[7:0],I0_a1_c1,_$_U6_out[3:0],I0_a0};
mantle_wire__typeBitIn14 _$_U2 (
    .in(_$_U2_in),
    .out(_$_U2_out)
);
assign _$_U3_out = {_$_U9_out[7:0],I1_a1_c1,_$_U8_out[3:0],I1_a0};
mantle_wire__typeBitIn14 _$_U3 (
    .in(_$_U3_in),
    .out(_$_U3_out)
);
assign _$_U4_in = coreir_commonlib_mux2x14_inst0_out;
mantle_wire__typeBit14 _$_U4 (
    .in(_$_U4_in),
    .out(_$_U4_out)
);
assign _$_U6_in = I0_a1_c0;
mantle_wire__typeBit4 _$_U6 (
    .in(_$_U6_in),
    .out(_$_U6_out)
);
assign _$_U7_in = I0_a2;
mantle_wire__typeBit8 _$_U7 (
    .in(_$_U7_in),
    .out(_$_U7_out)
);
assign _$_U8_in = I1_a1_c0;
mantle_wire__typeBit4 _$_U8 (
    .in(_$_U8_in),
    .out(_$_U8_out)
);
assign _$_U9_in = I1_a2;
mantle_wire__typeBit8 _$_U9 (
    .in(_$_U9_in),
    .out(_$_U9_out)
);
assign coreir_commonlib_mux2x14_inst0_in_data[1] = _$_U3_in;
assign coreir_commonlib_mux2x14_inst0_in_data[0] = _$_U2_in;
assign coreir_commonlib_mux2x14_inst0_in_sel[0] = S;
commonlib_muxn__N2__width14 coreir_commonlib_mux2x14_inst0 (
    .in_data(coreir_commonlib_mux2x14_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x14_inst0_in_sel),
    .out(coreir_commonlib_mux2x14_inst0_out)
);
assign O_a0 = _$_U4_out[0];
assign O_a1_c0 = _$_U10_in;
assign O_a1_c1 = _$_U4_out[5];
assign O_a2 = _$_U11_in;
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
wire Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a0;
wire [3:0] Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a1_c0;
wire Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a1_c1;
wire [7:0] Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a2;
wire Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a0;
wire [3:0] Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a1_c0;
wire Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a1_c1;
wire [7:0] Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a2;
wire Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a0;
wire [3:0] Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c0;
wire Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c1;
wire [7:0] Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a2;
wire Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_S;
assign Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a0 = self_a_O_a0;
assign Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a1_c0 = self_a_O_a1_c0;
assign Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a1_c1 = self_a_O_a1_c1;
assign Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a2 = self_a_O_a2;
assign Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a0 = a_a0;
assign Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a1_c0 = a_a1_c0;
assign Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a1_c1 = a_a1_c1;
assign Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a2 = a_a2;
assign Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_S = b;
Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8 Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0 (
    .I0_a0(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a0),
    .I0_a1_c0(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a1_c0),
    .I0_a1_c1(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a1_c1),
    .I0_a2(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I0_a2),
    .I1_a0(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a0),
    .I1_a1_c0(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a1_c0),
    .I1_a1_c1(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a1_c1),
    .I1_a2(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_I1_a2),
    .O_a0(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a0),
    .O_a1_c0(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c0),
    .O_a1_c1(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c1),
    .O_a2(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a2),
    .S(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_S)
);
assign O0_a0 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a0;
assign O0_a1_c0 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c0;
assign O0_a1_c1 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c1;
assign O0_a2 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a2;
assign O1_a0 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a0;
assign O1_a1_c0 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c0;
assign O1_a1_c1 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c1;
assign O1_a2 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a2;
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

module DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue (
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
    .init(1'h0),
    .width(1)
) reg_PR_inst0 (
    .clk(reg_PR_inst0_clk),
    .arst(reg_PR_inst0_arst),
    .in(reg_PR_inst0_in),
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
wire DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_I;
wire DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O;
wire DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_CLK;
wire DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_ASYNCRESET;
wire DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_I;
wire DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O;
wire DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_CLK;
wire DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_ASYNCRESET;
wire TestNestedProductReg_comb_inst0_O0_a0;
wire [3:0] TestNestedProductReg_comb_inst0_O0_a1_c0;
wire TestNestedProductReg_comb_inst0_O0_a1_c1;
wire [7:0] TestNestedProductReg_comb_inst0_O0_a2;
wire TestNestedProductReg_comb_inst0_O1_a0;
wire [3:0] TestNestedProductReg_comb_inst0_O1_a1_c0;
wire TestNestedProductReg_comb_inst0_O1_a1_c1;
wire [7:0] TestNestedProductReg_comb_inst0_O1_a2;
wire TestNestedProductReg_comb_inst0_a_a0;
wire [3:0] TestNestedProductReg_comb_inst0_a_a1_c0;
wire TestNestedProductReg_comb_inst0_a_a1_c1;
wire [7:0] TestNestedProductReg_comb_inst0_a_a2;
wire TestNestedProductReg_comb_inst0_b;
wire TestNestedProductReg_comb_inst0_self_a_O_a0;
wire [3:0] TestNestedProductReg_comb_inst0_self_a_O_a1_c0;
wire TestNestedProductReg_comb_inst0_self_a_O_a1_c1;
wire [7:0] TestNestedProductReg_comb_inst0_self_a_O_a2;
wire reg_PR_inst0_clk;
wire reg_PR_inst0_arst;
wire [3:0] reg_PR_inst0_in;
wire [3:0] reg_PR_inst0_out;
wire reg_PR_inst1_clk;
wire reg_PR_inst1_arst;
wire [7:0] reg_PR_inst1_in;
wire [7:0] reg_PR_inst1_out;
assign DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_I = TestNestedProductReg_comb_inst0_O0_a1_c1;
assign DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_CLK = CLK;
assign DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_ASYNCRESET = ASYNCRESET;
DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0 (
    .I(DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_I),
    .O(DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O),
    .CLK(DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_CLK),
    .ASYNCRESET(DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_ASYNCRESET)
);
assign DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_I = TestNestedProductReg_comb_inst0_O0_a0;
assign DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_CLK = CLK;
assign DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_ASYNCRESET = ASYNCRESET;
DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0 (
    .I(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_I),
    .O(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O),
    .CLK(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_CLK),
    .ASYNCRESET(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_ASYNCRESET)
);
assign TestNestedProductReg_comb_inst0_a_a0 = a_a0;
assign TestNestedProductReg_comb_inst0_a_a1_c0 = a_a1_c0;
assign TestNestedProductReg_comb_inst0_a_a1_c1 = a_a1_c1;
assign TestNestedProductReg_comb_inst0_a_a2 = a_a2;
assign TestNestedProductReg_comb_inst0_b = b;
assign TestNestedProductReg_comb_inst0_self_a_O_a0 = DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O;
assign TestNestedProductReg_comb_inst0_self_a_O_a1_c0 = reg_PR_inst0_out;
assign TestNestedProductReg_comb_inst0_self_a_O_a1_c1 = DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O;
assign TestNestedProductReg_comb_inst0_self_a_O_a2 = reg_PR_inst1_out;
TestNestedProductReg_comb TestNestedProductReg_comb_inst0 (
    .O0_a0(TestNestedProductReg_comb_inst0_O0_a0),
    .O0_a1_c0(TestNestedProductReg_comb_inst0_O0_a1_c0),
    .O0_a1_c1(TestNestedProductReg_comb_inst0_O0_a1_c1),
    .O0_a2(TestNestedProductReg_comb_inst0_O0_a2),
    .O1_a0(TestNestedProductReg_comb_inst0_O1_a0),
    .O1_a1_c0(TestNestedProductReg_comb_inst0_O1_a1_c0),
    .O1_a1_c1(TestNestedProductReg_comb_inst0_O1_a1_c1),
    .O1_a2(TestNestedProductReg_comb_inst0_O1_a2),
    .a_a0(TestNestedProductReg_comb_inst0_a_a0),
    .a_a1_c0(TestNestedProductReg_comb_inst0_a_a1_c0),
    .a_a1_c1(TestNestedProductReg_comb_inst0_a_a1_c1),
    .a_a2(TestNestedProductReg_comb_inst0_a_a2),
    .b(TestNestedProductReg_comb_inst0_b),
    .self_a_O_a0(TestNestedProductReg_comb_inst0_self_a_O_a0),
    .self_a_O_a1_c0(TestNestedProductReg_comb_inst0_self_a_O_a1_c0),
    .self_a_O_a1_c1(TestNestedProductReg_comb_inst0_self_a_O_a1_c1),
    .self_a_O_a2(TestNestedProductReg_comb_inst0_self_a_O_a2)
);
assign reg_PR_inst0_clk = CLK;
assign reg_PR_inst0_arst = ASYNCRESET;
assign reg_PR_inst0_in = TestNestedProductReg_comb_inst0_O0_a1_c0;
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(4'h3),
    .width(4)
) reg_PR_inst0 (
    .clk(reg_PR_inst0_clk),
    .arst(reg_PR_inst0_arst),
    .in(reg_PR_inst0_in),
    .out(reg_PR_inst0_out)
);
assign reg_PR_inst1_clk = CLK;
assign reg_PR_inst1_arst = ASYNCRESET;
assign reg_PR_inst1_in = TestNestedProductReg_comb_inst0_O0_a2;
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(8'h02),
    .width(8)
) reg_PR_inst1 (
    .clk(reg_PR_inst1_clk),
    .arst(reg_PR_inst1_arst),
    .in(reg_PR_inst1_in),
    .out(reg_PR_inst1_out)
);
assign O_a0 = TestNestedProductReg_comb_inst0_O1_a0;
assign O_a1_c0 = TestNestedProductReg_comb_inst0_O1_a1_c0;
assign O_a1_c1 = TestNestedProductReg_comb_inst0_O1_a1_c1;
assign O_a2 = TestNestedProductReg_comb_inst0_O1_a2;
endmodule

