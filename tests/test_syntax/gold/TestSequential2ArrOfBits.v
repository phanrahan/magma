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
wire [6:0] _$0_out;
wire [6:0] _$1_out;
wire [6:0] _$10_out;
wire [6:0] _$11_out;
wire [6:0] _$12_out;
wire [6:0] _$13_out;
wire [6:0] _$14_out;
wire [6:0] _$2_out;
wire [6:0] _$3_out;
wire [6:0] _$4_out;
wire [6:0] _$5_out;
wire [6:0] _$6_out;
wire [6:0] _$7_out;
wire [6:0] _$8_out;
wire [6:0] _$9_out;
wire [104:0] reg_P_inst0_out;
mantle_wire__typeBit7 _$0 (
    .in(I_0),
    .out(_$0_out)
);
mantle_wire__typeBit7 _$1 (
    .in(I_1),
    .out(_$1_out)
);
mantle_wire__typeBit7 _$10 (
    .in(I_5),
    .out(_$10_out)
);
mantle_wire__typeBit7 _$11 (
    .in(I_6),
    .out(_$11_out)
);
mantle_wire__typeBit7 _$12 (
    .in(I_7),
    .out(_$12_out)
);
mantle_wire__typeBit7 _$13 (
    .in(I_8),
    .out(_$13_out)
);
mantle_wire__typeBit7 _$14 (
    .in(I_9),
    .out(_$14_out)
);
mantle_wire__typeBitIn7 _$15 (
    .in(O_0),
    .out(reg_P_inst0_out[6:0])
);
mantle_wire__typeBitIn7 _$16 (
    .in(O_1),
    .out(reg_P_inst0_out[13:7])
);
mantle_wire__typeBitIn7 _$17 (
    .in(O_10),
    .out(reg_P_inst0_out[76:70])
);
mantle_wire__typeBitIn7 _$18 (
    .in(O_11),
    .out(reg_P_inst0_out[83:77])
);
mantle_wire__typeBitIn7 _$19 (
    .in(O_12),
    .out(reg_P_inst0_out[90:84])
);
mantle_wire__typeBit7 _$2 (
    .in(I_10),
    .out(_$2_out)
);
mantle_wire__typeBitIn7 _$20 (
    .in(O_13),
    .out(reg_P_inst0_out[97:91])
);
mantle_wire__typeBitIn7 _$21 (
    .in(O_14),
    .out(reg_P_inst0_out[104:98])
);
mantle_wire__typeBitIn7 _$22 (
    .in(O_2),
    .out(reg_P_inst0_out[20:14])
);
mantle_wire__typeBitIn7 _$23 (
    .in(O_3),
    .out(reg_P_inst0_out[27:21])
);
mantle_wire__typeBitIn7 _$24 (
    .in(O_4),
    .out(reg_P_inst0_out[34:28])
);
mantle_wire__typeBitIn7 _$25 (
    .in(O_5),
    .out(reg_P_inst0_out[41:35])
);
mantle_wire__typeBitIn7 _$26 (
    .in(O_6),
    .out(reg_P_inst0_out[48:42])
);
mantle_wire__typeBitIn7 _$27 (
    .in(O_7),
    .out(reg_P_inst0_out[55:49])
);
mantle_wire__typeBitIn7 _$28 (
    .in(O_8),
    .out(reg_P_inst0_out[62:56])
);
mantle_wire__typeBitIn7 _$29 (
    .in(O_9),
    .out(reg_P_inst0_out[69:63])
);
mantle_wire__typeBit7 _$3 (
    .in(I_11),
    .out(_$3_out)
);
mantle_wire__typeBit7 _$4 (
    .in(I_12),
    .out(_$4_out)
);
mantle_wire__typeBit7 _$5 (
    .in(I_13),
    .out(_$5_out)
);
mantle_wire__typeBit7 _$6 (
    .in(I_14),
    .out(_$6_out)
);
mantle_wire__typeBit7 _$7 (
    .in(I_2),
    .out(_$7_out)
);
mantle_wire__typeBit7 _$8 (
    .in(I_3),
    .out(_$8_out)
);
mantle_wire__typeBit7 _$9 (
    .in(I_4),
    .out(_$9_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(105'h000000000000000000000000000),
    .width(105)
) reg_P_inst0 (
    .clk(CLK),
    .in({_$6_out[6:0],_$5_out[6:0],_$4_out[6:0],_$3_out[6:0],_$2_out[6:0],_$14_out[6:0],_$13_out[6:0],_$12_out[6:0],_$11_out[6:0],_$10_out[6:0],_$9_out[6:0],_$8_out[6:0],_$7_out[6:0],_$1_out[6:0],_$0_out[6:0]}),
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

