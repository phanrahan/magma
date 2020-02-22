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

module ArrayOfBitsSeq_comb (
    input [1023:0] I_0,
    input [1023:0] I_1,
    input [1023:0] I_10,
    input [1023:0] I_11,
    input [1023:0] I_12,
    input [1023:0] I_13,
    input [1023:0] I_14,
    input [1023:0] I_2,
    input [1023:0] I_3,
    input [1023:0] I_4,
    input [1023:0] I_5,
    input [1023:0] I_6,
    input [1023:0] I_7,
    input [1023:0] I_8,
    input [1023:0] I_9,
    output [1023:0] O0_0,
    output [1023:0] O0_1,
    output [1023:0] O0_10,
    output [1023:0] O0_11,
    output [1023:0] O0_12,
    output [1023:0] O0_13,
    output [1023:0] O0_14,
    output [1023:0] O0_2,
    output [1023:0] O0_3,
    output [1023:0] O0_4,
    output [1023:0] O0_5,
    output [1023:0] O0_6,
    output [1023:0] O0_7,
    output [1023:0] O0_8,
    output [1023:0] O0_9,
    output [1023:0] O1_0,
    output [1023:0] O1_1,
    output [1023:0] O1_10,
    output [1023:0] O1_11,
    output [1023:0] O1_12,
    output [1023:0] O1_13,
    output [1023:0] O1_14,
    output [1023:0] O1_2,
    output [1023:0] O1_3,
    output [1023:0] O1_4,
    output [1023:0] O1_5,
    output [1023:0] O1_6,
    output [1023:0] O1_7,
    output [1023:0] O1_8,
    output [1023:0] O1_9,
    input [1023:0] self_register_array_O_0,
    input [1023:0] self_register_array_O_1,
    input [1023:0] self_register_array_O_10,
    input [1023:0] self_register_array_O_11,
    input [1023:0] self_register_array_O_12,
    input [1023:0] self_register_array_O_13,
    input [1023:0] self_register_array_O_14,
    input [1023:0] self_register_array_O_2,
    input [1023:0] self_register_array_O_3,
    input [1023:0] self_register_array_O_4,
    input [1023:0] self_register_array_O_5,
    input [1023:0] self_register_array_O_6,
    input [1023:0] self_register_array_O_7,
    input [1023:0] self_register_array_O_8,
    input [1023:0] self_register_array_O_9
);
assign O0_0 = I_0;
assign O0_1 = I_1;
assign O0_10 = I_10;
assign O0_11 = I_11;
assign O0_12 = I_12;
assign O0_13 = I_13;
assign O0_14 = I_14;
assign O0_2 = I_2;
assign O0_3 = I_3;
assign O0_4 = I_4;
assign O0_5 = I_5;
assign O0_6 = I_6;
assign O0_7 = I_7;
assign O0_8 = I_8;
assign O0_9 = I_9;
assign O1_0 = self_register_array_O_0;
assign O1_1 = self_register_array_O_1;
assign O1_10 = self_register_array_O_10;
assign O1_11 = self_register_array_O_11;
assign O1_12 = self_register_array_O_12;
assign O1_13 = self_register_array_O_13;
assign O1_14 = self_register_array_O_14;
assign O1_2 = self_register_array_O_2;
assign O1_3 = self_register_array_O_3;
assign O1_4 = self_register_array_O_4;
assign O1_5 = self_register_array_O_5;
assign O1_6 = self_register_array_O_6;
assign O1_7 = self_register_array_O_7;
assign O1_8 = self_register_array_O_8;
assign O1_9 = self_register_array_O_9;
endmodule

module ArrayOfBitsSeq (
    input ASYNCRESET,
    input CLK,
    input [1023:0] I_0,
    input [1023:0] I_1,
    input [1023:0] I_10,
    input [1023:0] I_11,
    input [1023:0] I_12,
    input [1023:0] I_13,
    input [1023:0] I_14,
    input [1023:0] I_2,
    input [1023:0] I_3,
    input [1023:0] I_4,
    input [1023:0] I_5,
    input [1023:0] I_6,
    input [1023:0] I_7,
    input [1023:0] I_8,
    input [1023:0] I_9,
    output [1023:0] O_0,
    output [1023:0] O_1,
    output [1023:0] O_10,
    output [1023:0] O_11,
    output [1023:0] O_12,
    output [1023:0] O_13,
    output [1023:0] O_14,
    output [1023:0] O_2,
    output [1023:0] O_3,
    output [1023:0] O_4,
    output [1023:0] O_5,
    output [1023:0] O_6,
    output [1023:0] O_7,
    output [1023:0] O_8,
    output [1023:0] O_9
);
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_0;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_1;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_10;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_11;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_12;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_13;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_14;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_2;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_3;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_4;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_5;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_6;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_7;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_8;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O0_9;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_0;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_1;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_10;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_11;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_12;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_13;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_14;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_2;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_3;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_4;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_5;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_6;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_7;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_8;
wire [1023:0] ArrayOfBitsSeq_comb_inst0_O1_9;
wire [1023:0] reg_PR_inst0_out;
wire [1023:0] reg_PR_inst1_out;
wire [1023:0] reg_PR_inst10_out;
wire [1023:0] reg_PR_inst11_out;
wire [1023:0] reg_PR_inst12_out;
wire [1023:0] reg_PR_inst13_out;
wire [1023:0] reg_PR_inst14_out;
wire [1023:0] reg_PR_inst2_out;
wire [1023:0] reg_PR_inst3_out;
wire [1023:0] reg_PR_inst4_out;
wire [1023:0] reg_PR_inst5_out;
wire [1023:0] reg_PR_inst6_out;
wire [1023:0] reg_PR_inst7_out;
wire [1023:0] reg_PR_inst8_out;
wire [1023:0] reg_PR_inst9_out;
ArrayOfBitsSeq_comb ArrayOfBitsSeq_comb_inst0 (
    .I_0(I_0),
    .I_1(I_1),
    .I_10(I_10),
    .I_11(I_11),
    .I_12(I_12),
    .I_13(I_13),
    .I_14(I_14),
    .I_2(I_2),
    .I_3(I_3),
    .I_4(I_4),
    .I_5(I_5),
    .I_6(I_6),
    .I_7(I_7),
    .I_8(I_8),
    .I_9(I_9),
    .O0_0(ArrayOfBitsSeq_comb_inst0_O0_0),
    .O0_1(ArrayOfBitsSeq_comb_inst0_O0_1),
    .O0_10(ArrayOfBitsSeq_comb_inst0_O0_10),
    .O0_11(ArrayOfBitsSeq_comb_inst0_O0_11),
    .O0_12(ArrayOfBitsSeq_comb_inst0_O0_12),
    .O0_13(ArrayOfBitsSeq_comb_inst0_O0_13),
    .O0_14(ArrayOfBitsSeq_comb_inst0_O0_14),
    .O0_2(ArrayOfBitsSeq_comb_inst0_O0_2),
    .O0_3(ArrayOfBitsSeq_comb_inst0_O0_3),
    .O0_4(ArrayOfBitsSeq_comb_inst0_O0_4),
    .O0_5(ArrayOfBitsSeq_comb_inst0_O0_5),
    .O0_6(ArrayOfBitsSeq_comb_inst0_O0_6),
    .O0_7(ArrayOfBitsSeq_comb_inst0_O0_7),
    .O0_8(ArrayOfBitsSeq_comb_inst0_O0_8),
    .O0_9(ArrayOfBitsSeq_comb_inst0_O0_9),
    .O1_0(ArrayOfBitsSeq_comb_inst0_O1_0),
    .O1_1(ArrayOfBitsSeq_comb_inst0_O1_1),
    .O1_10(ArrayOfBitsSeq_comb_inst0_O1_10),
    .O1_11(ArrayOfBitsSeq_comb_inst0_O1_11),
    .O1_12(ArrayOfBitsSeq_comb_inst0_O1_12),
    .O1_13(ArrayOfBitsSeq_comb_inst0_O1_13),
    .O1_14(ArrayOfBitsSeq_comb_inst0_O1_14),
    .O1_2(ArrayOfBitsSeq_comb_inst0_O1_2),
    .O1_3(ArrayOfBitsSeq_comb_inst0_O1_3),
    .O1_4(ArrayOfBitsSeq_comb_inst0_O1_4),
    .O1_5(ArrayOfBitsSeq_comb_inst0_O1_5),
    .O1_6(ArrayOfBitsSeq_comb_inst0_O1_6),
    .O1_7(ArrayOfBitsSeq_comb_inst0_O1_7),
    .O1_8(ArrayOfBitsSeq_comb_inst0_O1_8),
    .O1_9(ArrayOfBitsSeq_comb_inst0_O1_9),
    .self_register_array_O_0(reg_PR_inst0_out),
    .self_register_array_O_1(reg_PR_inst1_out),
    .self_register_array_O_10(reg_PR_inst10_out),
    .self_register_array_O_11(reg_PR_inst11_out),
    .self_register_array_O_12(reg_PR_inst12_out),
    .self_register_array_O_13(reg_PR_inst13_out),
    .self_register_array_O_14(reg_PR_inst14_out),
    .self_register_array_O_2(reg_PR_inst2_out),
    .self_register_array_O_3(reg_PR_inst3_out),
    .self_register_array_O_4(reg_PR_inst4_out),
    .self_register_array_O_5(reg_PR_inst5_out),
    .self_register_array_O_6(reg_PR_inst6_out),
    .self_register_array_O_7(reg_PR_inst7_out),
    .self_register_array_O_8(reg_PR_inst8_out),
    .self_register_array_O_9(reg_PR_inst9_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst0 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_0),
    .out(reg_PR_inst0_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst1 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_1),
    .out(reg_PR_inst1_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst10 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_10),
    .out(reg_PR_inst10_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst11 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_11),
    .out(reg_PR_inst11_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst12 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_12),
    .out(reg_PR_inst12_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst13 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_13),
    .out(reg_PR_inst13_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst14 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_14),
    .out(reg_PR_inst14_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst2 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_2),
    .out(reg_PR_inst2_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst3 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_3),
    .out(reg_PR_inst3_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst4 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_4),
    .out(reg_PR_inst4_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst5 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_5),
    .out(reg_PR_inst5_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst6 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_6),
    .out(reg_PR_inst6_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst7 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_7),
    .out(reg_PR_inst7_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst8 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_8),
    .out(reg_PR_inst8_out)
);
coreir_reg_arst #(
    .arst_posedge(1'b1),
    .clk_posedge(1'b1),
    .init(1024'h0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),
    .width(1024)
) reg_PR_inst9 (
    .clk(CLK),
    .arst(ASYNCRESET),
    .in(ArrayOfBitsSeq_comb_inst0_O0_9),
    .out(reg_PR_inst9_out)
);
assign O_0 = ArrayOfBitsSeq_comb_inst0_O1_0;
assign O_1 = ArrayOfBitsSeq_comb_inst0_O1_1;
assign O_10 = ArrayOfBitsSeq_comb_inst0_O1_10;
assign O_11 = ArrayOfBitsSeq_comb_inst0_O1_11;
assign O_12 = ArrayOfBitsSeq_comb_inst0_O1_12;
assign O_13 = ArrayOfBitsSeq_comb_inst0_O1_13;
assign O_14 = ArrayOfBitsSeq_comb_inst0_O1_14;
assign O_2 = ArrayOfBitsSeq_comb_inst0_O1_2;
assign O_3 = ArrayOfBitsSeq_comb_inst0_O1_3;
assign O_4 = ArrayOfBitsSeq_comb_inst0_O1_4;
assign O_5 = ArrayOfBitsSeq_comb_inst0_O1_5;
assign O_6 = ArrayOfBitsSeq_comb_inst0_O1_6;
assign O_7 = ArrayOfBitsSeq_comb_inst0_O1_7;
assign O_8 = ArrayOfBitsSeq_comb_inst0_O1_8;
assign O_9 = ArrayOfBitsSeq_comb_inst0_O1_9;
endmodule

