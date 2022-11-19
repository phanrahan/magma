module coreir_wire #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = in;
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

module Register (
    input CLK,
    input [9:0] I_0_x,
    input [9:0] I_1_x,
    input [9:0] I_2_x,
    input [9:0] I_3_x,
    input [9:0] I_4_x,
    input [9:0] I_5_x,
    input [9:0] I_6_x,
    input [9:0] I_7_x,
    input [9:0] I_8_x,
    input [9:0] I_9_x,
    output [9:0] O_0_x,
    output [9:0] O_1_x,
    output [9:0] O_2_x,
    output [9:0] O_3_x,
    output [9:0] O_4_x,
    output [9:0] O_5_x,
    output [9:0] O_6_x,
    output [9:0] O_7_x,
    output [9:0] O_8_x,
    output [9:0] O_9_x
);
wire [99:0] reg_P100_inst0_out;
wire [99:0] reg_P100_inst0_in;
assign reg_P100_inst0_in = {I_9_x,I_8_x,I_7_x,I_6_x,I_5_x,I_4_x,I_3_x,I_2_x,I_1_x,I_0_x};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(100'h0000000000000000000000000),
    .width(100)
) reg_P100_inst0 (
    .clk(CLK),
    .in(reg_P100_inst0_in),
    .out(reg_P100_inst0_out)
);
assign O_0_x = {reg_P100_inst0_out[9],reg_P100_inst0_out[8],reg_P100_inst0_out[7],reg_P100_inst0_out[6],reg_P100_inst0_out[5],reg_P100_inst0_out[4],reg_P100_inst0_out[3],reg_P100_inst0_out[2],reg_P100_inst0_out[1],reg_P100_inst0_out[0]};
assign O_1_x = {reg_P100_inst0_out[19],reg_P100_inst0_out[18],reg_P100_inst0_out[17],reg_P100_inst0_out[16],reg_P100_inst0_out[15],reg_P100_inst0_out[14],reg_P100_inst0_out[13],reg_P100_inst0_out[12],reg_P100_inst0_out[11],reg_P100_inst0_out[10]};
assign O_2_x = {reg_P100_inst0_out[29],reg_P100_inst0_out[28],reg_P100_inst0_out[27],reg_P100_inst0_out[26],reg_P100_inst0_out[25],reg_P100_inst0_out[24],reg_P100_inst0_out[23],reg_P100_inst0_out[22],reg_P100_inst0_out[21],reg_P100_inst0_out[20]};
assign O_3_x = {reg_P100_inst0_out[39],reg_P100_inst0_out[38],reg_P100_inst0_out[37],reg_P100_inst0_out[36],reg_P100_inst0_out[35],reg_P100_inst0_out[34],reg_P100_inst0_out[33],reg_P100_inst0_out[32],reg_P100_inst0_out[31],reg_P100_inst0_out[30]};
assign O_4_x = {reg_P100_inst0_out[49],reg_P100_inst0_out[48],reg_P100_inst0_out[47],reg_P100_inst0_out[46],reg_P100_inst0_out[45],reg_P100_inst0_out[44],reg_P100_inst0_out[43],reg_P100_inst0_out[42],reg_P100_inst0_out[41],reg_P100_inst0_out[40]};
assign O_5_x = {reg_P100_inst0_out[59],reg_P100_inst0_out[58],reg_P100_inst0_out[57],reg_P100_inst0_out[56],reg_P100_inst0_out[55],reg_P100_inst0_out[54],reg_P100_inst0_out[53],reg_P100_inst0_out[52],reg_P100_inst0_out[51],reg_P100_inst0_out[50]};
assign O_6_x = {reg_P100_inst0_out[69],reg_P100_inst0_out[68],reg_P100_inst0_out[67],reg_P100_inst0_out[66],reg_P100_inst0_out[65],reg_P100_inst0_out[64],reg_P100_inst0_out[63],reg_P100_inst0_out[62],reg_P100_inst0_out[61],reg_P100_inst0_out[60]};
assign O_7_x = {reg_P100_inst0_out[79],reg_P100_inst0_out[78],reg_P100_inst0_out[77],reg_P100_inst0_out[76],reg_P100_inst0_out[75],reg_P100_inst0_out[74],reg_P100_inst0_out[73],reg_P100_inst0_out[72],reg_P100_inst0_out[71],reg_P100_inst0_out[70]};
assign O_8_x = {reg_P100_inst0_out[89],reg_P100_inst0_out[88],reg_P100_inst0_out[87],reg_P100_inst0_out[86],reg_P100_inst0_out[85],reg_P100_inst0_out[84],reg_P100_inst0_out[83],reg_P100_inst0_out[82],reg_P100_inst0_out[81],reg_P100_inst0_out[80]};
assign O_9_x = {reg_P100_inst0_out[99],reg_P100_inst0_out[98],reg_P100_inst0_out[97],reg_P100_inst0_out[96],reg_P100_inst0_out[95],reg_P100_inst0_out[94],reg_P100_inst0_out[93],reg_P100_inst0_out[92],reg_P100_inst0_out[91],reg_P100_inst0_out[90]};
endmodule

module A (
    input port_0,
    input port_1,
    input port_2,
    input port_3,
    input port_4,
    input port_5,
    input port_6,
    input port_7,
    input port_8,
    input port_9,
    input port_10,
    input port_11,
    input port_12,
    input port_13,
    input port_14,
    input port_15,
    input port_16,
    input port_17,
    input port_18,
    input port_19,
    input port_20,
    input port_21,
    input port_22,
    input port_23,
    input port_24,
    input port_25,
    input port_26,
    input port_27,
    input port_28,
    input port_29,
    input port_30,
    input port_31,
    input port_32,
    input port_33,
    input port_34,
    input port_35,
    input port_36,
    input port_37,
    input port_38,
    input port_39,
    input port_40,
    input port_41,
    input port_42,
    input port_43,
    input port_44,
    input port_45,
    input port_46,
    input port_47,
    input port_48,
    input port_49,
    input port_50,
    input port_51,
    input port_52,
    input port_53,
    input port_54,
    input port_55,
    input port_56,
    input port_57,
    input port_58,
    input port_59,
    input port_60,
    input port_61,
    input port_62,
    input port_63,
    input port_64,
    input port_65,
    input port_66,
    input port_67,
    input port_68,
    input port_69,
    input port_70,
    input port_71,
    input port_72,
    input port_73,
    input port_74,
    input port_75,
    input port_76,
    input port_77,
    input port_78,
    input port_79,
    input port_80,
    input port_81,
    input port_82,
    input port_83,
    input port_84,
    input port_85,
    input port_86,
    input port_87,
    input port_88,
    input port_89,
    input port_90,
    input port_91,
    input port_92,
    input port_93,
    input port_94,
    input port_95,
    input port_96,
    input port_97,
    input port_98,
    input port_99,
    input port_100
);
wire [9:0] Register_inst0_O_0_x;
wire [9:0] Register_inst0_O_1_x;
wire [9:0] Register_inst0_O_2_x;
wire [9:0] Register_inst0_O_3_x;
wire [9:0] Register_inst0_O_4_x;
wire [9:0] Register_inst0_O_5_x;
wire [9:0] Register_inst0_O_6_x;
wire [9:0] Register_inst0_O_7_x;
wire [9:0] Register_inst0_O_8_x;
wire [9:0] Register_inst0_O_9_x;
wire [9:0] Register_inst0_I_0_x;
assign Register_inst0_I_0_x = {port_9,port_8,port_7,port_6,port_5,port_4,port_3,port_2,port_1,port_0};
wire [9:0] Register_inst0_I_1_x;
assign Register_inst0_I_1_x = {port_19,port_18,port_17,port_16,port_15,port_14,port_13,port_12,port_11,port_10};
wire [9:0] Register_inst0_I_2_x;
assign Register_inst0_I_2_x = {port_29,port_28,port_27,port_26,port_25,port_24,port_23,port_22,port_21,port_20};
wire [9:0] Register_inst0_I_3_x;
assign Register_inst0_I_3_x = {port_39,port_38,port_37,port_36,port_35,port_34,port_33,port_32,port_31,port_30};
wire [9:0] Register_inst0_I_4_x;
assign Register_inst0_I_4_x = {port_49,port_48,port_47,port_46,port_45,port_44,port_43,port_42,port_41,port_40};
wire [9:0] Register_inst0_I_5_x;
assign Register_inst0_I_5_x = {port_59,port_58,port_57,port_56,port_55,port_54,port_53,port_52,port_51,port_50};
wire [9:0] Register_inst0_I_6_x;
assign Register_inst0_I_6_x = {port_69,port_68,port_67,port_66,port_65,port_64,port_63,port_62,port_61,port_60};
wire [9:0] Register_inst0_I_7_x;
assign Register_inst0_I_7_x = {port_79,port_78,port_77,port_76,port_75,port_74,port_73,port_72,port_71,port_70};
wire [9:0] Register_inst0_I_8_x;
assign Register_inst0_I_8_x = {port_89,port_88,port_87,port_86,port_85,port_84,port_83,port_82,port_81,port_80};
wire [9:0] Register_inst0_I_9_x;
assign Register_inst0_I_9_x = {port_99,port_98,port_97,port_96,port_95,port_94,port_93,port_92,port_91,port_90};
Register Register_inst0 (
    .CLK(port_100),
    .I_0_x(Register_inst0_I_0_x),
    .I_1_x(Register_inst0_I_1_x),
    .I_2_x(Register_inst0_I_2_x),
    .I_3_x(Register_inst0_I_3_x),
    .I_4_x(Register_inst0_I_4_x),
    .I_5_x(Register_inst0_I_5_x),
    .I_6_x(Register_inst0_I_6_x),
    .I_7_x(Register_inst0_I_7_x),
    .I_8_x(Register_inst0_I_8_x),
    .I_9_x(Register_inst0_I_9_x),
    .O_0_x(Register_inst0_O_0_x),
    .O_1_x(Register_inst0_O_1_x),
    .O_2_x(Register_inst0_O_2_x),
    .O_3_x(Register_inst0_O_3_x),
    .O_4_x(Register_inst0_O_4_x),
    .O_5_x(Register_inst0_O_5_x),
    .O_6_x(Register_inst0_O_6_x),
    .O_7_x(Register_inst0_O_7_x),
    .O_8_x(Register_inst0_O_8_x),
    .O_9_x(Register_inst0_O_9_x)
);
endmodule

module _Top (
    input I,
    input CLK
);
wire [9:0] x_0_x_out;
wire [9:0] x_1_x_out;
wire [9:0] x_2_x_out;
wire [9:0] x_3_x_out;
wire [9:0] x_4_x_out;
wire [9:0] x_5_x_out;
wire [9:0] x_6_x_out;
wire [9:0] x_7_x_out;
wire [9:0] x_8_x_out;
wire [9:0] x_9_x_out;
`ifdef COND
A A (
    .port_0(x_0_x_out[0]),
    .port_1(x_0_x_out[1]),
    .port_2(x_0_x_out[2]),
    .port_3(x_0_x_out[3]),
    .port_4(x_0_x_out[4]),
    .port_5(x_0_x_out[5]),
    .port_6(x_0_x_out[6]),
    .port_7(x_0_x_out[7]),
    .port_8(x_0_x_out[8]),
    .port_9(x_0_x_out[9]),
    .port_10(x_1_x_out[0]),
    .port_11(x_1_x_out[1]),
    .port_12(x_1_x_out[2]),
    .port_13(x_1_x_out[3]),
    .port_14(x_1_x_out[4]),
    .port_15(x_1_x_out[5]),
    .port_16(x_1_x_out[6]),
    .port_17(x_1_x_out[7]),
    .port_18(x_1_x_out[8]),
    .port_19(x_1_x_out[9]),
    .port_20(x_2_x_out[0]),
    .port_21(x_2_x_out[1]),
    .port_22(x_2_x_out[2]),
    .port_23(x_2_x_out[3]),
    .port_24(x_2_x_out[4]),
    .port_25(x_2_x_out[5]),
    .port_26(x_2_x_out[6]),
    .port_27(x_2_x_out[7]),
    .port_28(x_2_x_out[8]),
    .port_29(x_2_x_out[9]),
    .port_30(x_3_x_out[0]),
    .port_31(x_3_x_out[1]),
    .port_32(x_3_x_out[2]),
    .port_33(x_3_x_out[3]),
    .port_34(x_3_x_out[4]),
    .port_35(x_3_x_out[5]),
    .port_36(x_3_x_out[6]),
    .port_37(x_3_x_out[7]),
    .port_38(x_3_x_out[8]),
    .port_39(x_3_x_out[9]),
    .port_40(x_4_x_out[0]),
    .port_41(x_4_x_out[1]),
    .port_42(x_4_x_out[2]),
    .port_43(x_4_x_out[3]),
    .port_44(x_4_x_out[4]),
    .port_45(x_4_x_out[5]),
    .port_46(x_4_x_out[6]),
    .port_47(x_4_x_out[7]),
    .port_48(x_4_x_out[8]),
    .port_49(x_4_x_out[9]),
    .port_50(x_5_x_out[0]),
    .port_51(x_5_x_out[1]),
    .port_52(x_5_x_out[2]),
    .port_53(x_5_x_out[3]),
    .port_54(x_5_x_out[4]),
    .port_55(x_5_x_out[5]),
    .port_56(x_5_x_out[6]),
    .port_57(x_5_x_out[7]),
    .port_58(x_5_x_out[8]),
    .port_59(x_5_x_out[9]),
    .port_60(x_6_x_out[0]),
    .port_61(x_6_x_out[1]),
    .port_62(x_6_x_out[2]),
    .port_63(x_6_x_out[3]),
    .port_64(x_6_x_out[4]),
    .port_65(x_6_x_out[5]),
    .port_66(x_6_x_out[6]),
    .port_67(x_6_x_out[7]),
    .port_68(x_6_x_out[8]),
    .port_69(x_6_x_out[9]),
    .port_70(x_7_x_out[0]),
    .port_71(x_7_x_out[1]),
    .port_72(x_7_x_out[2]),
    .port_73(x_7_x_out[3]),
    .port_74(x_7_x_out[4]),
    .port_75(x_7_x_out[5]),
    .port_76(x_7_x_out[6]),
    .port_77(x_7_x_out[7]),
    .port_78(x_7_x_out[8]),
    .port_79(x_7_x_out[9]),
    .port_80(x_8_x_out[0]),
    .port_81(x_8_x_out[1]),
    .port_82(x_8_x_out[2]),
    .port_83(x_8_x_out[3]),
    .port_84(x_8_x_out[4]),
    .port_85(x_8_x_out[5]),
    .port_86(x_8_x_out[6]),
    .port_87(x_8_x_out[7]),
    .port_88(x_8_x_out[8]),
    .port_89(x_8_x_out[9]),
    .port_90(x_9_x_out[0]),
    .port_91(x_9_x_out[1]),
    .port_92(x_9_x_out[2]),
    .port_93(x_9_x_out[3]),
    .port_94(x_9_x_out[4]),
    .port_95(x_9_x_out[5]),
    .port_96(x_9_x_out[6]),
    .port_97(x_9_x_out[7]),
    .port_98(x_9_x_out[8]),
    .port_99(x_9_x_out[9]),
    .port_100(CLK)
);
`endif
wire [9:0] x_0_x_in;
assign x_0_x_in = {I,I,I,I,I,I,I,I,I,I};
coreir_wire #(
    .width(10)
) x_0_x (
    .in(x_0_x_in),
    .out(x_0_x_out)
);
wire [9:0] x_1_x_in;
assign x_1_x_in = {I,I,I,I,I,I,I,I,I,I};
coreir_wire #(
    .width(10)
) x_1_x (
    .in(x_1_x_in),
    .out(x_1_x_out)
);
wire [9:0] x_2_x_in;
assign x_2_x_in = {I,I,I,I,I,I,I,I,I,I};
coreir_wire #(
    .width(10)
) x_2_x (
    .in(x_2_x_in),
    .out(x_2_x_out)
);
wire [9:0] x_3_x_in;
assign x_3_x_in = {I,I,I,I,I,I,I,I,I,I};
coreir_wire #(
    .width(10)
) x_3_x (
    .in(x_3_x_in),
    .out(x_3_x_out)
);
wire [9:0] x_4_x_in;
assign x_4_x_in = {I,I,I,I,I,I,I,I,I,I};
coreir_wire #(
    .width(10)
) x_4_x (
    .in(x_4_x_in),
    .out(x_4_x_out)
);
wire [9:0] x_5_x_in;
assign x_5_x_in = {I,I,I,I,I,I,I,I,I,I};
coreir_wire #(
    .width(10)
) x_5_x (
    .in(x_5_x_in),
    .out(x_5_x_out)
);
wire [9:0] x_6_x_in;
assign x_6_x_in = {I,I,I,I,I,I,I,I,I,I};
coreir_wire #(
    .width(10)
) x_6_x (
    .in(x_6_x_in),
    .out(x_6_x_out)
);
wire [9:0] x_7_x_in;
assign x_7_x_in = {I,I,I,I,I,I,I,I,I,I};
coreir_wire #(
    .width(10)
) x_7_x (
    .in(x_7_x_in),
    .out(x_7_x_out)
);
wire [9:0] x_8_x_in;
assign x_8_x_in = {I,I,I,I,I,I,I,I,I,I};
coreir_wire #(
    .width(10)
) x_8_x (
    .in(x_8_x_in),
    .out(x_8_x_out)
);
wire [9:0] x_9_x_in;
assign x_9_x_in = {I,I,I,I,I,I,I,I,I,I};
coreir_wire #(
    .width(10)
) x_9_x (
    .in(x_9_x_in),
    .out(x_9_x_out)
);
endmodule

