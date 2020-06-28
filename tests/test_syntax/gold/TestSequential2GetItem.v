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

module commonlib_muxn__N2__width7 (
    input [6:0] in_data_0,
    input [6:0] in_data_1,
    input [0:0] in_sel,
    output [6:0] out
);
assign out = in_sel[0] ? in_data_1 : in_data_0;
endmodule

module commonlib_muxn__N4__width7 (
    input [6:0] in_data_0,
    input [6:0] in_data_1,
    input [6:0] in_data_2,
    input [6:0] in_data_3,
    input [1:0] in_sel,
    output [6:0] out
);
wire [6:0] muxN_0_out;
wire [6:0] muxN_1_out;
commonlib_muxn__N2__width7 muxN_0 (
    .in_data_0(in_data_0),
    .in_data_1(in_data_1),
    .in_sel(in_sel[1 - 1:0]),
    .out(muxN_0_out)
);
commonlib_muxn__N2__width7 muxN_1 (
    .in_data_0(in_data_2),
    .in_data_1(in_data_3),
    .in_sel(in_sel[1 - 1:0]),
    .out(muxN_1_out)
);
assign out = in_sel[1] ? muxN_1_out : muxN_0_out;
endmodule

module commonlib_muxn__N8__width7 (
    input [6:0] in_data_0,
    input [6:0] in_data_1,
    input [6:0] in_data_2,
    input [6:0] in_data_3,
    input [6:0] in_data_4,
    input [6:0] in_data_5,
    input [6:0] in_data_6,
    input [6:0] in_data_7,
    input [2:0] in_sel,
    output [6:0] out
);
wire [6:0] muxN_0_out;
wire [6:0] muxN_1_out;
commonlib_muxn__N4__width7 muxN_0 (
    .in_data_0(in_data_0),
    .in_data_1(in_data_1),
    .in_data_2(in_data_2),
    .in_data_3(in_data_3),
    .in_sel(in_sel[2 - 1:0]),
    .out(muxN_0_out)
);
commonlib_muxn__N4__width7 muxN_1 (
    .in_data_0(in_data_4),
    .in_data_1(in_data_5),
    .in_data_2(in_data_6),
    .in_data_3(in_data_7),
    .in_sel(in_sel[2 - 1:0]),
    .out(muxN_1_out)
);
assign out = in_sel[2] ? muxN_1_out : muxN_0_out;
endmodule

module Register_unq1 (
    input [2:0] I,
    output [2:0] O,
    input CLK
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(3'h0),
    .width(3)
) reg_P_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Register (
    input CLK,
    input [6:0] I_0,
    input [6:0] I_1,
    input [6:0] I_2,
    input [6:0] I_3,
    input [6:0] I_4,
    input [6:0] I_5,
    input [6:0] I_6,
    input [6:0] I_7,
    output [6:0] O_0,
    output [6:0] O_1,
    output [6:0] O_2,
    output [6:0] O_3,
    output [6:0] O_4,
    output [6:0] O_5,
    output [6:0] O_6,
    output [6:0] O_7
);
wire [6:0] _$0_out;
wire [6:0] _$1_out;
wire [6:0] _$2_out;
wire [6:0] _$3_out;
wire [6:0] _$4_out;
wire [6:0] _$5_out;
wire [6:0] _$6_out;
wire [6:0] _$7_out;
wire [55:0] reg_P_inst0_out;
mantle_wire__typeBit7 _$0 (
    .in(I_0),
    .out(_$0_out)
);
mantle_wire__typeBit7 _$1 (
    .in(I_1),
    .out(_$1_out)
);
mantle_wire__typeBitIn7 _$10 (
    .in(O_2),
    .out(reg_P_inst0_out[20:14])
);
mantle_wire__typeBitIn7 _$11 (
    .in(O_3),
    .out(reg_P_inst0_out[27:21])
);
mantle_wire__typeBitIn7 _$12 (
    .in(O_4),
    .out(reg_P_inst0_out[34:28])
);
mantle_wire__typeBitIn7 _$13 (
    .in(O_5),
    .out(reg_P_inst0_out[41:35])
);
mantle_wire__typeBitIn7 _$14 (
    .in(O_6),
    .out(reg_P_inst0_out[48:42])
);
mantle_wire__typeBitIn7 _$15 (
    .in(O_7),
    .out(reg_P_inst0_out[55:49])
);
mantle_wire__typeBit7 _$2 (
    .in(I_2),
    .out(_$2_out)
);
mantle_wire__typeBit7 _$3 (
    .in(I_3),
    .out(_$3_out)
);
mantle_wire__typeBit7 _$4 (
    .in(I_4),
    .out(_$4_out)
);
mantle_wire__typeBit7 _$5 (
    .in(I_5),
    .out(_$5_out)
);
mantle_wire__typeBit7 _$6 (
    .in(I_6),
    .out(_$6_out)
);
mantle_wire__typeBit7 _$7 (
    .in(I_7),
    .out(_$7_out)
);
mantle_wire__typeBitIn7 _$8 (
    .in(O_0),
    .out(reg_P_inst0_out[6:0])
);
mantle_wire__typeBitIn7 _$9 (
    .in(O_1),
    .out(reg_P_inst0_out[13:7])
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(56'h00000000000000),
    .width(56)
) reg_P_inst0 (
    .clk(CLK),
    .in({_$7_out[6:0],_$6_out[6:0],_$5_out[6:0],_$4_out[6:0],_$3_out[6:0],_$2_out[6:0],_$1_out[6:0],_$0_out[6:0]}),
    .out(reg_P_inst0_out)
);
endmodule

module Mux8xOutBits7 (
    input [6:0] I0,
    input [6:0] I1,
    input [6:0] I2,
    input [6:0] I3,
    input [6:0] I4,
    input [6:0] I5,
    input [6:0] I6,
    input [6:0] I7,
    input [2:0] S,
    output [6:0] O
);
commonlib_muxn__N8__width7 coreir_commonlib_mux8x7_inst0 (
    .in_data_0(I0),
    .in_data_1(I1),
    .in_data_2(I2),
    .in_data_3(I3),
    .in_data_4(I4),
    .in_data_5(I5),
    .in_data_6(I6),
    .in_data_7(I7),
    .in_sel(S),
    .out(O)
);
endmodule

module Test2 (
    input CLK,
    input [6:0] I_0,
    input [6:0] I_1,
    input [6:0] I_2,
    input [6:0] I_3,
    input [6:0] I_4,
    input [6:0] I_5,
    input [6:0] I_6,
    input [6:0] I_7,
    output [6:0] O_0,
    output [6:0] O_1,
    input [2:0] index
);
wire [6:0] Register_inst0_O_0;
wire [6:0] Register_inst0_O_1;
wire [6:0] Register_inst0_O_2;
wire [6:0] Register_inst0_O_3;
wire [6:0] Register_inst0_O_4;
wire [6:0] Register_inst0_O_5;
wire [6:0] Register_inst0_O_6;
wire [6:0] Register_inst0_O_7;
wire [2:0] Register_inst1_O;
Mux8xOutBits7 Mux8xOutBits7_inst0 (
    .I0(Register_inst0_O_0),
    .I1(Register_inst0_O_1),
    .I2(Register_inst0_O_2),
    .I3(Register_inst0_O_3),
    .I4(Register_inst0_O_4),
    .I5(Register_inst0_O_5),
    .I6(Register_inst0_O_6),
    .I7(Register_inst0_O_7),
    .S(index),
    .O(O_0)
);
Mux8xOutBits7 Mux8xOutBits7_inst1 (
    .I0(Register_inst0_O_0),
    .I1(Register_inst0_O_1),
    .I2(Register_inst0_O_2),
    .I3(Register_inst0_O_3),
    .I4(Register_inst0_O_4),
    .I5(Register_inst0_O_5),
    .I6(Register_inst0_O_6),
    .I7(Register_inst0_O_7),
    .S(Register_inst1_O),
    .O(O_1)
);
Register Register_inst0 (
    .CLK(CLK),
    .I_0(I_0),
    .I_1(I_1),
    .I_2(I_2),
    .I_3(I_3),
    .I_4(I_4),
    .I_5(I_5),
    .I_6(I_6),
    .I_7(I_7),
    .O_0(Register_inst0_O_0),
    .O_1(Register_inst0_O_1),
    .O_2(Register_inst0_O_2),
    .O_3(Register_inst0_O_3),
    .O_4(Register_inst0_O_4),
    .O_5(Register_inst0_O_5),
    .O_6(Register_inst0_O_6),
    .O_7(Register_inst0_O_7)
);
Register_unq1 Register_inst1 (
    .I(index),
    .O(Register_inst1_O),
    .CLK(CLK)
);
endmodule

