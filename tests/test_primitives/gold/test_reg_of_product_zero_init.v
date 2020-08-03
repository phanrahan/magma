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

module mantle_wire__typeBitIn12 (
    output [11:0] in,
    input [11:0] out
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

module mantle_wire__typeBit12 (
    input [11:0] in,
    output [11:0] out
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

module commonlib_muxn__N2__width12 (
    input [11:0] in_data [1:0],
    input [0:0] in_sel,
    output [11:0] out
);
wire [11:0] _join_in0;
wire [11:0] _join_in1;
wire _join_sel;
wire [11:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(12)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xTuplex_Bits8_y_Bits4 (
    input [7:0] I0_x,
    input [3:0] I0_y,
    input [7:0] I1_x,
    input [3:0] I1_y,
    output [7:0] O_x,
    output [3:0] O_y,
    input S
);
wire [7:0] _$_U10_in;
wire [7:0] _$_U10_out;
wire [3:0] _$_U11_in;
wire [3:0] _$_U11_out;
wire [11:0] _$_U2_in;
wire [11:0] _$_U2_out;
wire [11:0] _$_U3_in;
wire [11:0] _$_U3_out;
wire [11:0] _$_U4_in;
wire [11:0] _$_U4_out;
wire [7:0] _$_U6_in;
wire [7:0] _$_U6_out;
wire [3:0] _$_U7_in;
wire [3:0] _$_U7_out;
wire [7:0] _$_U8_in;
wire [7:0] _$_U8_out;
wire [3:0] _$_U9_in;
wire [3:0] _$_U9_out;
wire [11:0] coreir_commonlib_mux2x12_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x12_inst0_in_sel;
wire [11:0] coreir_commonlib_mux2x12_inst0_out;
assign _$_U10_out = _$_U4_out[7:0];
mantle_wire__typeBitIn8 _$_U10 (
    .in(_$_U10_in),
    .out(_$_U10_out)
);
assign _$_U11_out = _$_U4_out[11:8];
mantle_wire__typeBitIn4 _$_U11 (
    .in(_$_U11_in),
    .out(_$_U11_out)
);
assign _$_U2_out = {_$_U7_out[3:0],_$_U6_out[7:0]};
mantle_wire__typeBitIn12 _$_U2 (
    .in(_$_U2_in),
    .out(_$_U2_out)
);
assign _$_U3_out = {_$_U9_out[3:0],_$_U8_out[7:0]};
mantle_wire__typeBitIn12 _$_U3 (
    .in(_$_U3_in),
    .out(_$_U3_out)
);
assign _$_U4_in = coreir_commonlib_mux2x12_inst0_out;
mantle_wire__typeBit12 _$_U4 (
    .in(_$_U4_in),
    .out(_$_U4_out)
);
assign _$_U6_in = I0_x;
mantle_wire__typeBit8 _$_U6 (
    .in(_$_U6_in),
    .out(_$_U6_out)
);
assign _$_U7_in = I0_y;
mantle_wire__typeBit4 _$_U7 (
    .in(_$_U7_in),
    .out(_$_U7_out)
);
assign _$_U8_in = I1_x;
mantle_wire__typeBit8 _$_U8 (
    .in(_$_U8_in),
    .out(_$_U8_out)
);
assign _$_U9_in = I1_y;
mantle_wire__typeBit4 _$_U9 (
    .in(_$_U9_in),
    .out(_$_U9_out)
);
assign coreir_commonlib_mux2x12_inst0_in_data = '{_$_U3_in,_$_U2_in};
assign coreir_commonlib_mux2x12_inst0_in_sel = S;
commonlib_muxn__N2__width12 coreir_commonlib_mux2x12_inst0 (
    .in_data(coreir_commonlib_mux2x12_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x12_inst0_in_sel),
    .out(coreir_commonlib_mux2x12_inst0_out)
);
assign O_x = _$_U10_in;
assign O_y = _$_U11_in;
endmodule

module Register (
    input CLK,
    input [7:0] I_x,
    input [3:0] I_y,
    output [7:0] O_x,
    output [3:0] O_y,
    input RESET
);
wire [7:0] Mux2xTuplex_Bits8_y_Bits4_inst0_I0_x;
wire [3:0] Mux2xTuplex_Bits8_y_Bits4_inst0_I0_y;
wire [7:0] Mux2xTuplex_Bits8_y_Bits4_inst0_I1_x;
wire [3:0] Mux2xTuplex_Bits8_y_Bits4_inst0_I1_y;
wire [7:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_x;
wire [3:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_y;
wire Mux2xTuplex_Bits8_y_Bits4_inst0_S;
wire [7:0] _$_U13_in;
wire [7:0] _$_U13_out;
wire [3:0] _$_U14_in;
wire [3:0] _$_U14_out;
wire [7:0] _$_U16_in;
wire [7:0] _$_U16_out;
wire [3:0] _$_U17_in;
wire [3:0] _$_U17_out;
wire [3:0] const_0_4_out;
wire [7:0] const_0_8_out;
wire reg_P_inst0_clk;
wire [11:0] reg_P_inst0_in;
wire [11:0] reg_P_inst0_out;
assign Mux2xTuplex_Bits8_y_Bits4_inst0_I0_x = I_x;
assign Mux2xTuplex_Bits8_y_Bits4_inst0_I0_y = I_y;
assign Mux2xTuplex_Bits8_y_Bits4_inst0_I1_x = const_0_8_out;
assign Mux2xTuplex_Bits8_y_Bits4_inst0_I1_y = const_0_4_out;
assign Mux2xTuplex_Bits8_y_Bits4_inst0_S = RESET;
Mux2xTuplex_Bits8_y_Bits4 Mux2xTuplex_Bits8_y_Bits4_inst0 (
    .I0_x(Mux2xTuplex_Bits8_y_Bits4_inst0_I0_x),
    .I0_y(Mux2xTuplex_Bits8_y_Bits4_inst0_I0_y),
    .I1_x(Mux2xTuplex_Bits8_y_Bits4_inst0_I1_x),
    .I1_y(Mux2xTuplex_Bits8_y_Bits4_inst0_I1_y),
    .O_x(Mux2xTuplex_Bits8_y_Bits4_inst0_O_x),
    .O_y(Mux2xTuplex_Bits8_y_Bits4_inst0_O_y),
    .S(Mux2xTuplex_Bits8_y_Bits4_inst0_S)
);
assign _$_U13_in = Mux2xTuplex_Bits8_y_Bits4_inst0_O_x;
mantle_wire__typeBit8 _$_U13 (
    .in(_$_U13_in),
    .out(_$_U13_out)
);
assign _$_U14_in = Mux2xTuplex_Bits8_y_Bits4_inst0_O_y;
mantle_wire__typeBit4 _$_U14 (
    .in(_$_U14_in),
    .out(_$_U14_out)
);
assign _$_U16_out = reg_P_inst0_out[7:0];
mantle_wire__typeBitIn8 _$_U16 (
    .in(_$_U16_in),
    .out(_$_U16_out)
);
assign _$_U17_out = reg_P_inst0_out[11:8];
mantle_wire__typeBitIn4 _$_U17 (
    .in(_$_U17_in),
    .out(_$_U17_out)
);
coreir_const #(
    .value(4'h0),
    .width(4)
) const_0_4 (
    .out(const_0_4_out)
);
coreir_const #(
    .value(8'h00),
    .width(8)
) const_0_8 (
    .out(const_0_8_out)
);
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = {_$_U14_out[3:0],_$_U13_out[7:0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(12'h000),
    .width(12)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O_x = _$_U16_in;
assign O_y = _$_U17_in;
endmodule

module test_reg_of_product_zero_init (
    input CLK,
    input [7:0] I_x,
    input [3:0] I_y,
    output [7:0] O_x,
    output [3:0] O_y,
    input RESET
);
wire Register_inst0_CLK;
wire [7:0] Register_inst0_I_x;
wire [3:0] Register_inst0_I_y;
wire [7:0] Register_inst0_O_x;
wire [3:0] Register_inst0_O_y;
wire Register_inst0_RESET;
assign Register_inst0_CLK = CLK;
assign Register_inst0_I_x = I_x;
assign Register_inst0_I_y = I_y;
assign Register_inst0_RESET = RESET;
Register Register_inst0 (
    .CLK(Register_inst0_CLK),
    .I_x(Register_inst0_I_x),
    .I_y(Register_inst0_I_y),
    .O_x(Register_inst0_O_x),
    .O_y(Register_inst0_O_y),
    .RESET(Register_inst0_RESET)
);
assign O_x = Register_inst0_O_x;
assign O_y = Register_inst0_O_y;
endmodule

