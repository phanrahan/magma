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
    input [11:0] in_data_0,
    input [11:0] in_data_1,
    input [0:0] in_sel,
    output [11:0] out
);
wire [11:0] _join_out;
coreir_mux #(
    .width(12)
) _join (
    .in0(in_data_0),
    .in1(in_data_1),
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
wire [11:0] _$0_in;
wire [11:0] _$1_in;
wire [11:0] _$2_out;
wire [7:0] _$3_out;
wire [3:0] _$4_out;
wire [7:0] _$5_out;
wire [3:0] _$6_out;
wire [7:0] _$7_in;
wire [3:0] _$8_in;
wire [11:0] coreir_commonlib_mux2x12_inst0_out;
mantle_wire__typeBitIn12 _$0 (
    .in(_$0_in),
    .out({_$4_out[3:0],_$3_out[7:0]})
);
mantle_wire__typeBitIn12 _$1 (
    .in(_$1_in),
    .out({_$6_out[3:0],_$5_out[7:0]})
);
mantle_wire__typeBit12 _$2 (
    .in(coreir_commonlib_mux2x12_inst0_out),
    .out(_$2_out)
);
mantle_wire__typeBit8 _$3 (
    .in(I0_x),
    .out(_$3_out)
);
mantle_wire__typeBit4 _$4 (
    .in(I0_y),
    .out(_$4_out)
);
mantle_wire__typeBit8 _$5 (
    .in(I1_x),
    .out(_$5_out)
);
mantle_wire__typeBit4 _$6 (
    .in(I1_y),
    .out(_$6_out)
);
mantle_wire__typeBitIn8 _$7 (
    .in(_$7_in),
    .out(_$2_out[7:0])
);
mantle_wire__typeBitIn4 _$8 (
    .in(_$8_in),
    .out(_$2_out[11:8])
);
commonlib_muxn__N2__width12 coreir_commonlib_mux2x12_inst0 (
    .in_data_0(_$0_in),
    .in_data_1(_$1_in),
    .in_sel(S),
    .out(coreir_commonlib_mux2x12_inst0_out)
);
assign O_x = _$7_in;
assign O_y = _$8_in;
endmodule

module Register (
    input CLK,
    input [7:0] I_x,
    input [3:0] I_y,
    output [7:0] O_x,
    output [3:0] O_y,
    input RESET
);
wire [7:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_x;
wire [3:0] Mux2xTuplex_Bits8_y_Bits4_inst0_O_y;
wire [7:0] _$0_out;
wire [3:0] _$1_out;
wire [7:0] _$2_in;
wire [3:0] _$3_in;
wire [3:0] const_0_4_out;
wire [7:0] const_0_8_out;
wire [11:0] reg_P_inst0_out;
Mux2xTuplex_Bits8_y_Bits4 Mux2xTuplex_Bits8_y_Bits4_inst0 (
    .I0_x(I_x),
    .I0_y(I_y),
    .I1_x(const_0_8_out),
    .I1_y(const_0_4_out),
    .O_x(Mux2xTuplex_Bits8_y_Bits4_inst0_O_x),
    .O_y(Mux2xTuplex_Bits8_y_Bits4_inst0_O_y),
    .S(RESET)
);
mantle_wire__typeBit8 _$0 (
    .in(Mux2xTuplex_Bits8_y_Bits4_inst0_O_x),
    .out(_$0_out)
);
mantle_wire__typeBit4 _$1 (
    .in(Mux2xTuplex_Bits8_y_Bits4_inst0_O_y),
    .out(_$1_out)
);
mantle_wire__typeBitIn8 _$2 (
    .in(_$2_in),
    .out(reg_P_inst0_out[7:0])
);
mantle_wire__typeBitIn4 _$3 (
    .in(_$3_in),
    .out(reg_P_inst0_out[11:8])
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
coreir_reg #(
    .clk_posedge(1'b1),
    .init(12'h000),
    .width(12)
) reg_P_inst0 (
    .clk(CLK),
    .in({_$1_out[3:0],_$0_out[7:0]}),
    .out(reg_P_inst0_out)
);
assign O_x = _$2_in;
assign O_y = _$3_in;
endmodule

module test_reg_of_product_zero_init (
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

