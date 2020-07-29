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

module Register (
    input CLK,
    input [6:0] I_0,
    input [6:0] I_1,
    input [6:0] I_10,
    input [6:0] I_11,
    input [6:0] I_12,
    input [6:0] I_13,
    input [6:0] I_14,
    input [6:0] I_2,
    input [6:0] I_3,
    input [6:0] I_4,
    input [6:0] I_5,
    input [6:0] I_6,
    input [6:0] I_7,
    input [6:0] I_8,
    input [6:0] I_9,
    output [6:0] O_0,
    output [6:0] O_1,
    output [6:0] O_10,
    output [6:0] O_11,
    output [6:0] O_12,
    output [6:0] O_13,
    output [6:0] O_14,
    output [6:0] O_2,
    output [6:0] O_3,
    output [6:0] O_4,
    output [6:0] O_5,
    output [6:0] O_6,
    output [6:0] O_7,
    output [6:0] O_8,
    output [6:0] O_9
);
wire [104:0] reg_P_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(105'h000000000000000000000000000),
    .width(105)
) reg_P_inst0 (
    .clk(CLK),
    .in({I_14[6:0],I_13[6:0],I_12[6:0],I_11[6:0],I_10[6:0],I_9[6:0],I_8[6:0],I_7[6:0],I_6[6:0],I_5[6:0],I_4[6:0],I_3[6:0],I_2[6:0],I_1[6:0],I_0[6:0]}),
    .out(reg_P_inst0_out)
);
assign O_0 = reg_P_inst0_out[6:0];
assign O_1 = reg_P_inst0_out[13:7];
assign O_10 = reg_P_inst0_out[76:70];
assign O_11 = reg_P_inst0_out[83:77];
assign O_12 = reg_P_inst0_out[90:84];
assign O_13 = reg_P_inst0_out[97:91];
assign O_14 = reg_P_inst0_out[104:98];
assign O_2 = reg_P_inst0_out[20:14];
assign O_3 = reg_P_inst0_out[27:21];
assign O_4 = reg_P_inst0_out[34:28];
assign O_5 = reg_P_inst0_out[41:35];
assign O_6 = reg_P_inst0_out[48:42];
assign O_7 = reg_P_inst0_out[55:49];
assign O_8 = reg_P_inst0_out[62:56];
assign O_9 = reg_P_inst0_out[69:63];
endmodule

module Test2 (
    input CLK,
    input [6:0] I_0,
    input [6:0] I_1,
    input [6:0] I_10,
    input [6:0] I_11,
    input [6:0] I_12,
    input [6:0] I_13,
    input [6:0] I_14,
    input [6:0] I_2,
    input [6:0] I_3,
    input [6:0] I_4,
    input [6:0] I_5,
    input [6:0] I_6,
    input [6:0] I_7,
    input [6:0] I_8,
    input [6:0] I_9,
    output [6:0] O_0,
    output [6:0] O_1,
    output [6:0] O_10,
    output [6:0] O_11,
    output [6:0] O_12,
    output [6:0] O_13,
    output [6:0] O_14,
    output [6:0] O_2,
    output [6:0] O_3,
    output [6:0] O_4,
    output [6:0] O_5,
    output [6:0] O_6,
    output [6:0] O_7,
    output [6:0] O_8,
    output [6:0] O_9
);
Register Register_inst0 (
    .CLK(CLK),
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
    .O_0(O_0),
    .O_1(O_1),
    .O_10(O_10),
    .O_11(O_11),
    .O_12(O_12),
    .O_13(O_13),
    .O_14(O_14),
    .O_2(O_2),
    .O_3(O_3),
    .O_4(O_4),
    .O_5(O_5),
    .O_6(O_6),
    .O_7(O_7),
    .O_8(O_8),
    .O_9(O_9)
);
endmodule

