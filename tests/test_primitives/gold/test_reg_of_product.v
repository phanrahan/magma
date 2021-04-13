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
wire [11:0] _join_out;
coreir_mux #(
    .width(12)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
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
wire [11:0] coreir_commonlib_mux2x12_inst0_out_unq1;
wire [11:0] coreir_commonlib_mux2x12_inst0_in_data_0_in;
wire [11:0] coreir_commonlib_mux2x12_inst0_in_data_1_in;
wire [11:0] coreir_commonlib_mux2x12_inst0_out_out;
wire [7:0] self_I0_x_out;
wire [3:0] self_I0_y_out;
wire [7:0] self_I1_x_out;
wire [3:0] self_I1_y_out;
wire [7:0] self_O_x_in;
wire [3:0] self_O_y_in;
wire [11:0] coreir_commonlib_mux2x12_inst0_in_data [1:0];
assign coreir_commonlib_mux2x12_inst0_in_data[1] = coreir_commonlib_mux2x12_inst0_in_data_1_in;
assign coreir_commonlib_mux2x12_inst0_in_data[0] = coreir_commonlib_mux2x12_inst0_in_data_0_in;
commonlib_muxn__N2__width12 coreir_commonlib_mux2x12_inst0 (
    .in_data(coreir_commonlib_mux2x12_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x12_inst0_out_unq1)
);
wire [11:0] coreir_commonlib_mux2x12_inst0_in_data_0_out;
assign coreir_commonlib_mux2x12_inst0_in_data_0_out = {self_I0_y_out[3:0],self_I0_x_out[7:0]};
mantle_wire__typeBitIn12 coreir_commonlib_mux2x12_inst0_in_data_0 (
    .in(coreir_commonlib_mux2x12_inst0_in_data_0_in),
    .out(coreir_commonlib_mux2x12_inst0_in_data_0_out)
);
wire [11:0] coreir_commonlib_mux2x12_inst0_in_data_1_out;
assign coreir_commonlib_mux2x12_inst0_in_data_1_out = {self_I1_y_out[3:0],self_I1_x_out[7:0]};
mantle_wire__typeBitIn12 coreir_commonlib_mux2x12_inst0_in_data_1 (
    .in(coreir_commonlib_mux2x12_inst0_in_data_1_in),
    .out(coreir_commonlib_mux2x12_inst0_in_data_1_out)
);
mantle_wire__typeBit12 coreir_commonlib_mux2x12_inst0_out (
    .in(coreir_commonlib_mux2x12_inst0_out_unq1),
    .out(coreir_commonlib_mux2x12_inst0_out_out)
);
mantle_wire__typeBit8 self_I0_x (
    .in(I0_x),
    .out(self_I0_x_out)
);
mantle_wire__typeBit4 self_I0_y (
    .in(I0_y),
    .out(self_I0_y_out)
);
mantle_wire__typeBit8 self_I1_x (
    .in(I1_x),
    .out(self_I1_x_out)
);
mantle_wire__typeBit4 self_I1_y (
    .in(I1_y),
    .out(self_I1_y_out)
);
mantle_wire__typeBitIn8 self_O_x (
    .in(self_O_x_in),
    .out(coreir_commonlib_mux2x12_inst0_out_out[7:0])
);
mantle_wire__typeBitIn4 self_O_y (
    .in(self_O_y_in),
    .out(coreir_commonlib_mux2x12_inst0_out_out[11:8])
);
assign O_x = self_O_x_in;
assign O_y = self_O_y_in;
endmodule

module Register (
    input CLK,
    input [7:0] I_x,
    input [3:0] I_y,
    output [7:0] O_x,
    output [3:0] O_y,
    input RESET
);
wire [7:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_x_unq1;
wire [3:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_y_unq1;
wire [7:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_x_out;
wire [3:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_y_out;
wire [3:0] const_10_4_out;
wire [7:0] const_222_8_out;
wire [11:0] reg_P12_inst0_out;
wire [7:0] self_O_x_in;
wire [3:0] self_O_y_in;
Mux2xTuplex_Bits8_y_Bits4 Mux2xTuplex_Bits8_y_Bits4_inst0 (
    .I0_x(I_x),
    .I0_y(I_y),
    .I1_x(const_222_8_out),
    .I1_y(const_10_4_out),
    .O_x(Mux2xTuplex_Bits8_y_Bits4_inst0_O_x_unq1),
    .O_y(Mux2xTuplex_Bits8_y_Bits4_inst0_O_y_unq1),
    .S(RESET)
);
mantle_wire__typeBit8 Mux2xTuplex_Bits8_y_Bits4_inst0_O_x (
    .in(Mux2xTuplex_Bits8_y_Bits4_inst0_O_x_unq1),
    .out(Mux2xTuplex_Bits8_y_Bits4_inst0_O_x_out)
);
mantle_wire__typeBit4 Mux2xTuplex_Bits8_y_Bits4_inst0_O_y (
    .in(Mux2xTuplex_Bits8_y_Bits4_inst0_O_y_unq1),
    .out(Mux2xTuplex_Bits8_y_Bits4_inst0_O_y_out)
);
coreir_const #(
    .value(4'ha),
    .width(4)
) const_10_4 (
    .out(const_10_4_out)
);
coreir_const #(
    .value(8'hde),
    .width(8)
) const_222_8 (
    .out(const_222_8_out)
);
wire [11:0] reg_P12_inst0_in;
assign reg_P12_inst0_in = {Mux2xTuplex_Bits8_y_Bits4_inst0_O_y_out[3:0],Mux2xTuplex_Bits8_y_Bits4_inst0_O_x_out[7:0]};
coreir_reg #(
    .clk_posedge(1'b1),
    .init(12'hade),
    .width(12)
) reg_P12_inst0 (
    .clk(CLK),
    .in(reg_P12_inst0_in),
    .out(reg_P12_inst0_out)
);
mantle_wire__typeBitIn8 self_O_x (
    .in(self_O_x_in),
    .out(reg_P12_inst0_out[7:0])
);
mantle_wire__typeBitIn4 self_O_y (
    .in(self_O_y_in),
    .out(reg_P12_inst0_out[11:8])
);
assign O_x = self_O_x_in;
assign O_y = self_O_y_in;
endmodule

module test_reg_of_product (
    input CLK,
    input [7:0] I_x,
    input [3:0] I_y,
    output [7:0] O_x,
    output [3:0] O_y,
    input RESET
);
wire [7:0] Register_inst0_O_x;
wire [3:0] Register_inst0_O_y;
Register Register_inst0 (
    .CLK(CLK),
    .I_x(I_x),
    .I_y(I_y),
    .O_x(Register_inst0_O_x),
    .O_y(Register_inst0_O_y),
    .RESET(RESET)
);
assign O_x = Register_inst0_O_x;
assign O_y = Register_inst0_O_y;
endmodule

