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
wire [6:0] _$_U10_out;
wire [6:0] _$_U11_out;
wire [6:0] _$_U12_out;
wire [6:0] _$_U13_out;
wire [6:0] _$_U14_out;
wire [6:0] _$_U15_out;
wire [6:0] _$_U16_out;
wire [6:0] _$_U9_out;
wire [55:0] reg_P_inst0_out;
mantle_wire__typeBit7 _$_U10 (
    .in(I_1),
    .out(_$_U10_out)
);
mantle_wire__typeBit7 _$_U11 (
    .in(I_2),
    .out(_$_U11_out)
);
mantle_wire__typeBit7 _$_U12 (
    .in(I_3),
    .out(_$_U12_out)
);
mantle_wire__typeBit7 _$_U13 (
    .in(I_4),
    .out(_$_U13_out)
);
mantle_wire__typeBit7 _$_U14 (
    .in(I_5),
    .out(_$_U14_out)
);
mantle_wire__typeBit7 _$_U15 (
    .in(I_6),
    .out(_$_U15_out)
);
mantle_wire__typeBit7 _$_U16 (
    .in(I_7),
    .out(_$_U16_out)
);
mantle_wire__typeBitIn7 _$_U17 (
    .in(O_0),
    .out(reg_P_inst0_out[6:0])
);
mantle_wire__typeBitIn7 _$_U18 (
    .in(O_1),
    .out(reg_P_inst0_out[13:7])
);
mantle_wire__typeBitIn7 _$_U19 (
    .in(O_2),
    .out(reg_P_inst0_out[20:14])
);
mantle_wire__typeBitIn7 _$_U20 (
    .in(O_3),
    .out(reg_P_inst0_out[27:21])
);
mantle_wire__typeBitIn7 _$_U21 (
    .in(O_4),
    .out(reg_P_inst0_out[34:28])
);
mantle_wire__typeBitIn7 _$_U22 (
    .in(O_5),
    .out(reg_P_inst0_out[41:35])
);
mantle_wire__typeBitIn7 _$_U23 (
    .in(O_6),
    .out(reg_P_inst0_out[48:42])
);
mantle_wire__typeBitIn7 _$_U24 (
    .in(O_7),
    .out(reg_P_inst0_out[55:49])
);
mantle_wire__typeBit7 _$_U9 (
    .in(I_0),
    .out(_$_U9_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(56'h00000000000000),
    .width(56)
) reg_P_inst0 (
    .clk(CLK),
    .in({_$_U16_out[6:0],_$_U15_out[6:0],_$_U14_out[6:0],_$_U13_out[6:0],_$_U12_out[6:0],_$_U11_out[6:0],_$_U10_out[6:0],_$_U9_out[6:0]}),
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
reg [6:0] coreir_commonlib_mux8x7_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux8x7_inst0_out = I0;
end else if (S == 1) begin
    coreir_commonlib_mux8x7_inst0_out = I1;
end else if (S == 2) begin
    coreir_commonlib_mux8x7_inst0_out = I2;
end else if (S == 3) begin
    coreir_commonlib_mux8x7_inst0_out = I3;
end else if (S == 4) begin
    coreir_commonlib_mux8x7_inst0_out = I4;
end else if (S == 5) begin
    coreir_commonlib_mux8x7_inst0_out = I5;
end else if (S == 6) begin
    coreir_commonlib_mux8x7_inst0_out = I6;
end else begin
    coreir_commonlib_mux8x7_inst0_out = I7;
end
end

assign O = coreir_commonlib_mux8x7_inst0_out;
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

