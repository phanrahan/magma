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

module commonlib_muxn__N2__width8 (
    input [7:0] in_data [1:0],
    input [0:0] in_sel,
    output [7:0] out
);
wire [7:0] _join_out;
coreir_mux #(
    .width(8)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xBits8 (
    input [7:0] I0,
    input [7:0] I1,
    input S,
    output [7:0] O
);
wire [7:0] coreir_commonlib_mux2x8_inst0_out;
wire [7:0] coreir_commonlib_mux2x8_inst0_in_data [1:0];
assign coreir_commonlib_mux2x8_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x8_inst0_in_data[0] = I0;
commonlib_muxn__N2__width8 coreir_commonlib_mux2x8_inst0 (
    .in_data(coreir_commonlib_mux2x8_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x8_inst0_out)
);
assign O = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Register (
    input [7:0] I,
    output [7:0] O,
    input CLK,
    input RESET
);
wire [7:0] Mux2xBits8_inst0_O;
wire [7:0] const_222_8_out;
wire [7:0] reg_P8_inst0_out;
Mux2xBits8 Mux2xBits8_inst0 (
    .I0(I),
    .I1(const_222_8_out),
    .S(RESET),
    .O(Mux2xBits8_inst0_O)
);
coreir_const #(
    .value(8'hde),
    .width(8)
) const_222_8 (
    .out(const_222_8_out)
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'hde),
    .width(8)
) reg_P8_inst0 (
    .clk(CLK),
    .in(Mux2xBits8_inst0_O),
    .out(reg_P8_inst0_out)
);
assign O = reg_P8_inst0_out;
endmodule

module test_basic_reg_BitsMeta (
    input [7:0] I,
    output [7:0] O,
    input CLK,
    input RESET
);
wire [7:0] Register_inst0_O;
Register Register_inst0 (
    .I(I),
    .O(Register_inst0_O),
    .CLK(CLK),
    .RESET(RESET)
);
assign O = Register_inst0_O;
endmodule

