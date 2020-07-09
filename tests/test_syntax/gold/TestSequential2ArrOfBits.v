module mantle_wire__typeBitIn7 (
    output [6:0] in,
    input [6:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit7 (
    input [6:0] in,
    output [6:0] out
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
wire [6:0] _$_U1_out;
wire [6:0] _$_U10_out;
wire [6:0] _$_U11_out;
wire [6:0] _$_U12_out;
wire [6:0] _$_U13_out;
wire [6:0] _$_U14_out;
wire [6:0] _$_U15_out;
wire [6:0] _$_U2_out;
wire [6:0] _$_U3_out;
wire [6:0] _$_U4_out;
wire [6:0] _$_U5_out;
wire [6:0] _$_U6_out;
wire [6:0] _$_U7_out;
wire [6:0] _$_U8_out;
wire [6:0] _$_U9_out;
wire [104:0] reg_P_inst0_out;
mantle_wire__typeBit7 _$_U1 (
    .in(I_0),
    .out(_$_U1_out)
);
mantle_wire__typeBit7 _$_U10 (
    .in(I_4),
    .out(_$_U10_out)
);
mantle_wire__typeBit7 _$_U11 (
    .in(I_5),
    .out(_$_U11_out)
);
mantle_wire__typeBit7 _$_U12 (
    .in(I_6),
    .out(_$_U12_out)
);
mantle_wire__typeBit7 _$_U13 (
    .in(I_7),
    .out(_$_U13_out)
);
mantle_wire__typeBit7 _$_U14 (
    .in(I_8),
    .out(_$_U14_out)
);
mantle_wire__typeBit7 _$_U15 (
    .in(I_9),
    .out(_$_U15_out)
);
mantle_wire__typeBitIn7 _$_U16 (
    .in(O_0),
    .out(reg_P_inst0_out[6:0])
);
mantle_wire__typeBitIn7 _$_U17 (
    .in(O_1),
    .out(reg_P_inst0_out[13:7])
);
mantle_wire__typeBitIn7 _$_U18 (
    .in(O_10),
    .out(reg_P_inst0_out[76:70])
);
mantle_wire__typeBitIn7 _$_U19 (
    .in(O_11),
    .out(reg_P_inst0_out[83:77])
);
mantle_wire__typeBit7 _$_U2 (
    .in(I_1),
    .out(_$_U2_out)
);
mantle_wire__typeBitIn7 _$_U20 (
    .in(O_12),
    .out(reg_P_inst0_out[90:84])
);
mantle_wire__typeBitIn7 _$_U21 (
    .in(O_13),
    .out(reg_P_inst0_out[97:91])
);
mantle_wire__typeBitIn7 _$_U22 (
    .in(O_14),
    .out(reg_P_inst0_out[104:98])
);
mantle_wire__typeBitIn7 _$_U23 (
    .in(O_2),
    .out(reg_P_inst0_out[20:14])
);
mantle_wire__typeBitIn7 _$_U24 (
    .in(O_3),
    .out(reg_P_inst0_out[27:21])
);
mantle_wire__typeBitIn7 _$_U25 (
    .in(O_4),
    .out(reg_P_inst0_out[34:28])
);
mantle_wire__typeBitIn7 _$_U26 (
    .in(O_5),
    .out(reg_P_inst0_out[41:35])
);
mantle_wire__typeBitIn7 _$_U27 (
    .in(O_6),
    .out(reg_P_inst0_out[48:42])
);
mantle_wire__typeBitIn7 _$_U28 (
    .in(O_7),
    .out(reg_P_inst0_out[55:49])
);
mantle_wire__typeBitIn7 _$_U29 (
    .in(O_8),
    .out(reg_P_inst0_out[62:56])
);
mantle_wire__typeBit7 _$_U3 (
    .in(I_10),
    .out(_$_U3_out)
);
mantle_wire__typeBitIn7 _$_U30 (
    .in(O_9),
    .out(reg_P_inst0_out[69:63])
);
mantle_wire__typeBit7 _$_U4 (
    .in(I_11),
    .out(_$_U4_out)
);
mantle_wire__typeBit7 _$_U5 (
    .in(I_12),
    .out(_$_U5_out)
);
mantle_wire__typeBit7 _$_U6 (
    .in(I_13),
    .out(_$_U6_out)
);
mantle_wire__typeBit7 _$_U7 (
    .in(I_14),
    .out(_$_U7_out)
);
mantle_wire__typeBit7 _$_U8 (
    .in(I_2),
    .out(_$_U8_out)
);
mantle_wire__typeBit7 _$_U9 (
    .in(I_3),
    .out(_$_U9_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(105'h000000000000000000000000000),
    .width(105)
) reg_P_inst0 (
    .clk(CLK),
    .in({_$_U7_out[6:0],_$_U6_out[6:0],_$_U5_out[6:0],_$_U4_out[6:0],_$_U3_out[6:0],_$_U15_out[6:0],_$_U14_out[6:0],_$_U13_out[6:0],_$_U12_out[6:0],_$_U11_out[6:0],_$_U10_out[6:0],_$_U9_out[6:0],_$_U8_out[6:0],_$_U2_out[6:0],_$_U1_out[6:0]}),
    .out(reg_P_inst0_out)
);
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

