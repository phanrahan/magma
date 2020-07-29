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

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module commonlib_muxn__N2__width24 (
    input [23:0] in_data_0,
    input [23:0] in_data_1,
    input [0:0] in_sel,
    output [23:0] out
);
wire [23:0] _join_out;
coreir_mux #(
    .width(24)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xArray3_Bits8 (
    input [7:0] I0_0,
    input [7:0] I0_1,
    input [7:0] I0_2,
    input [7:0] I1_0,
    input [7:0] I1_1,
    input [7:0] I1_2,
    output [7:0] O_0,
    output [7:0] O_1,
    output [7:0] O_2,
    input S
);
wire [7:0] _$_U10_out;
wire [7:0] _$_U11_out;
wire [7:0] _$_U12_in;
wire [7:0] _$_U13_in;
wire [7:0] _$_U14_in;
wire [23:0] _$_U2_in;
wire [23:0] _$_U3_in;
wire [23:0] _$_U4_out;
wire [7:0] _$_U6_out;
wire [7:0] _$_U7_out;
wire [7:0] _$_U8_out;
wire [7:0] _$_U9_out;
wire [23:0] coreir_commonlib_mux2x24_inst0_out;
mantle_wire__typeBit8 _$_U10 (
    .in(I1_1),
    .out(_$_U10_out)
);
mantle_wire__typeBit8 _$_U11 (
    .in(I1_2),
    .out(_$_U11_out)
);
mantle_wire__typeBitIn8 _$_U12 (
    .in(_$_U12_in),
    .out(_$_U4_out[7:0])
);
mantle_wire__typeBitIn8 _$_U13 (
    .in(_$_U13_in),
    .out(_$_U4_out[15:8])
);
mantle_wire__typeBitIn8 _$_U14 (
    .in(_$_U14_in),
    .out(_$_U4_out[23:16])
);
mantle_wire__typeBitIn24 _$_U2 (
    .in(_$_U2_in),
    .out({_$_U8_out[7:0],_$_U7_out[7:0],_$_U6_out[7:0]})
);
mantle_wire__typeBitIn24 _$_U3 (
    .in(_$_U3_in),
    .out({_$_U11_out[7:0],_$_U10_out[7:0],_$_U9_out[7:0]})
);
mantle_wire__typeBit24 _$_U4 (
    .in(coreir_commonlib_mux2x24_inst0_out),
    .out(_$_U4_out)
);
mantle_wire__typeBit8 _$_U6 (
    .in(I0_0),
    .out(_$_U6_out)
);
mantle_wire__typeBit8 _$_U7 (
    .in(I0_1),
    .out(_$_U7_out)
);
mantle_wire__typeBit8 _$_U8 (
    .in(I0_2),
    .out(_$_U8_out)
);
mantle_wire__typeBit8 _$_U9 (
    .in(I1_0),
    .out(_$_U9_out)
);
commonlib_muxn__N2__width24 coreir_commonlib_mux2x24_inst0 (
    .in_data_0(_$_U2_in),
    .in_data_1(_$_U3_in),
    .in_sel(S),
    .out(coreir_commonlib_mux2x24_inst0_out)
);
assign O_0 = _$_U12_in;
assign O_1 = _$_U13_in;
assign O_2 = _$_U14_in;
endmodule

module Register (
    input CLK,
    input [7:0] I_0,
    input [7:0] I_1,
    input [7:0] I_2,
    output [7:0] O_0,
    output [7:0] O_1,
    output [7:0] O_2,
    input RESET
);
wire [7:0] Mux2xArray3_Bits8_inst0_O_0;
wire [7:0] Mux2xArray3_Bits8_inst0_O_1;
wire [7:0] Mux2xArray3_Bits8_inst0_O_2;
wire [7:0] _$_U16_out;
wire [7:0] _$_U17_out;
wire [7:0] _$_U18_out;
wire [7:0] _$_U20_in;
wire [7:0] _$_U21_in;
wire [7:0] _$_U22_in;
wire [7:0] const_173_8_out;
wire [7:0] const_190_8_out;
wire [7:0] const_222_8_out;
wire [23:0] reg_P_inst0_out;
Mux2xArray3_Bits8 Mux2xArray3_Bits8_inst0 (
    .I0_0(I_0),
    .I0_1(I_1),
    .I0_2(I_2),
    .I1_0(const_222_8_out),
    .I1_1(const_173_8_out),
    .I1_2(const_190_8_out),
    .O_0(Mux2xArray3_Bits8_inst0_O_0),
    .O_1(Mux2xArray3_Bits8_inst0_O_1),
    .O_2(Mux2xArray3_Bits8_inst0_O_2),
    .S(RESET)
);
mantle_wire__typeBit8 _$_U16 (
    .in(Mux2xArray3_Bits8_inst0_O_0),
    .out(_$_U16_out)
);
mantle_wire__typeBit8 _$_U17 (
    .in(Mux2xArray3_Bits8_inst0_O_1),
    .out(_$_U17_out)
);
mantle_wire__typeBit8 _$_U18 (
    .in(Mux2xArray3_Bits8_inst0_O_2),
    .out(_$_U18_out)
);
mantle_wire__typeBitIn8 _$_U20 (
    .in(_$_U20_in),
    .out(reg_P_inst0_out[7:0])
);
mantle_wire__typeBitIn8 _$_U21 (
    .in(_$_U21_in),
    .out(reg_P_inst0_out[15:8])
);
mantle_wire__typeBitIn8 _$_U22 (
    .in(_$_U22_in),
    .out(reg_P_inst0_out[23:16])
);
coreir_const #(
    .value(8'had),
    .width(8)
) const_173_8 (
    .out(const_173_8_out)
);
coreir_const #(
    .value(8'hbe),
    .width(8)
) const_190_8 (
    .out(const_190_8_out)
);
coreir_const #(
    .value(8'hde),
    .width(8)
) const_222_8 (
    .out(const_222_8_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(24'h000000),
    .width(24)
) reg_P_inst0 (
    .clk(CLK),
    .in({_$_U18_out[7:0],_$_U17_out[7:0],_$_U16_out[7:0]}),
    .out(reg_P_inst0_out)
);
assign O_0 = _$_U20_in;
assign O_1 = _$_U21_in;
assign O_2 = _$_U22_in;
endmodule

module test_reg_of_nested_array (
    input CLK,
    input [7:0] I_0,
    input [7:0] I_1,
    input [7:0] I_2,
    output [7:0] O_0,
    output [7:0] O_1,
    output [7:0] O_2,
    input RESET
);
wire [7:0] Register_inst0_O_0;
wire [7:0] Register_inst0_O_1;
wire [7:0] Register_inst0_O_2;
Register Register_inst0 (
    .CLK(CLK),
    .I_0(I_0),
    .I_1(I_1),
    .I_2(I_2),
    .O_0(Register_inst0_O_0),
    .O_1(Register_inst0_O_1),
    .O_2(Register_inst0_O_2),
    .RESET(RESET)
);
assign O_0 = Register_inst0_O_0;
assign O_1 = Register_inst0_O_1;
assign O_2 = Register_inst0_O_2;
endmodule

