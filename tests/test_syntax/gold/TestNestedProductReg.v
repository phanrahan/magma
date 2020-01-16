// Module `Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8` defined externally
module coreir_reg_arst #(parameter width = 1, parameter arst_posedge = 1, parameter clk_posedge = 1, parameter init = 1) (input clk, input arst, input [width-1:0] in, output [width-1:0] out);
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

module TestNestedProductReg_comb (output O0_a0, output [3:0] O0_a1_c0, output O0_a1_c1, output [7:0] O0_a2, output O1_a0, output [3:0] O1_a1_c0, output O1_a1_c1, output [7:0] O1_a2, input a_a0, input [3:0] a_a1_c0, input a_a1_c1, input [7:0] a_a2, input b, input self_a_O_a0, input [3:0] self_a_O_a1_c0, input self_a_O_a1_c1, input [7:0] self_a_O_a2);
wire Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a0;
wire [3:0] Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c0;
wire Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c1;
wire [7:0] Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a2;
Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8 Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0(.I0_a0(self_a_O_a0), .I0_a1_c0(self_a_O_a1_c0), .I0_a1_c1(self_a_O_a1_c1), .I0_a2(self_a_O_a2), .I1_a0(a_a0), .I1_a1_c0(a_a1_c0), .I1_a1_c1(a_a1_c1), .I1_a2(a_a2), .O_a0(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a0), .O_a1_c0(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c0), .O_a1_c1(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c1), .O_a2(Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a2), .S(b));
assign O0_a0 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a0;
assign O0_a1_c0 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c0;
assign O0_a1_c1 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c1;
assign O0_a2 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a2;
assign O1_a0 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a0;
assign O1_a1_c0 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c0;
assign O1_a1_c1 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a1_c1;
assign O1_a2 = Mux2xTuplea0_OutBit_a1_Tuplec0_OutUInt4_c1_OutBit_a2_OutSInt8_inst0_O_a2;
endmodule

module DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue (input ASYNCRESET, input CLK, input I, output O);
wire [0:0] reg_PR_inst0_out;
coreir_reg_arst #(.arst_posedge(1'b1), .clk_posedge(1'b1), .init(1'h1), .width(1)) reg_PR_inst0(.arst(ASYNCRESET), .clk(CLK), .in(I), .out(reg_PR_inst0_out));
assign O = reg_PR_inst0_out[0];
endmodule

module DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue (input ASYNCRESET, input CLK, input I, output O);
wire [0:0] reg_PR_inst0_out;
coreir_reg_arst #(.arst_posedge(1'b1), .clk_posedge(1'b1), .init(1'h0), .width(1)) reg_PR_inst0(.arst(ASYNCRESET), .clk(CLK), .in(I), .out(reg_PR_inst0_out));
assign O = reg_PR_inst0_out[0];
endmodule

module TestNestedProductReg (input ASYNCRESET, input CLK, output O_a0, output [3:0] O_a1_c0, output O_a1_c1, output [7:0] O_a2, input a_a0, input [3:0] a_a1_c0, input a_a1_c1, input [7:0] a_a2, input b);
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
DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0(.ASYNCRESET(ASYNCRESET), .CLK(CLK), .I(TestNestedProductReg_comb_inst0_O0_a1_c1), .O(DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O));
DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0(.ASYNCRESET(ASYNCRESET), .CLK(CLK), .I(TestNestedProductReg_comb_inst0_O0_a0), .O(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O));
TestNestedProductReg_comb TestNestedProductReg_comb_inst0(.O0_a0(TestNestedProductReg_comb_inst0_O0_a0), .O0_a1_c0(TestNestedProductReg_comb_inst0_O0_a1_c0), .O0_a1_c1(TestNestedProductReg_comb_inst0_O0_a1_c1), .O0_a2(TestNestedProductReg_comb_inst0_O0_a2), .O1_a0(TestNestedProductReg_comb_inst0_O1_a0), .O1_a1_c0(TestNestedProductReg_comb_inst0_O1_a1_c0), .O1_a1_c1(TestNestedProductReg_comb_inst0_O1_a1_c1), .O1_a2(TestNestedProductReg_comb_inst0_O1_a2), .a_a0(a_a0), .a_a1_c0(a_a1_c0), .a_a1_c1(a_a1_c1), .a_a2(a_a2), .b(b), .self_a_O_a0(DFF_initTrue_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O), .self_a_O_a1_c0(reg_PR_inst0_out), .self_a_O_a1_c1(DFF_initFalse_has_ceFalse_has_resetFalse_has_async_resetTrue_inst0_O), .self_a_O_a2(reg_PR_inst1_out));
coreir_reg_arst #(.arst_posedge(1'b1), .clk_posedge(1'b1), .init(4'h3), .width(4)) reg_PR_inst0(.arst(ASYNCRESET), .clk(CLK), .in(TestNestedProductReg_comb_inst0_O0_a1_c0), .out(reg_PR_inst0_out));
coreir_reg_arst #(.arst_posedge(1'b1), .clk_posedge(1'b1), .init(8'h02), .width(8)) reg_PR_inst1(.arst(ASYNCRESET), .clk(CLK), .in(TestNestedProductReg_comb_inst0_O0_a2), .out(reg_PR_inst1_out));
assign O_a0 = TestNestedProductReg_comb_inst0_O1_a0;
assign O_a1_c0 = TestNestedProductReg_comb_inst0_O1_a1_c0;
assign O_a1_c1 = TestNestedProductReg_comb_inst0_O1_a1_c1;
assign O_a2 = TestNestedProductReg_comb_inst0_O1_a2;
endmodule

