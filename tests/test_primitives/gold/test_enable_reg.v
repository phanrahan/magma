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
wire [7:0] _join_in0;
wire [7:0] _join_in1;
wire _join_sel;
wire [7:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(8)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
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
wire [7:0] coreir_commonlib_mux2x8_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x8_inst0_in_sel;
wire [7:0] coreir_commonlib_mux2x8_inst0_out;
assign coreir_commonlib_mux2x8_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x8_inst0_in_data[0] = I0;
assign coreir_commonlib_mux2x8_inst0_in_sel[0] = S;
commonlib_muxn__N2__width8 coreir_commonlib_mux2x8_inst0 (
    .in_data(coreir_commonlib_mux2x8_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x8_inst0_in_sel),
    .out(coreir_commonlib_mux2x8_inst0_out)
);
assign O = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Register (
    input [7:0] I,
    output [7:0] O,
    input CLK,
    input CE,
    input RESET
);
wire [7:0] Mux2xBits8_inst0_I0;
wire [7:0] Mux2xBits8_inst0_I1;
wire Mux2xBits8_inst0_S;
wire [7:0] Mux2xBits8_inst0_O;
wire [7:0] const_222_8_out;
wire [7:0] enable_mux_I0;
wire [7:0] enable_mux_I1;
wire enable_mux_S;
wire [7:0] enable_mux_O;
wire reg_P_inst0_clk;
wire [7:0] reg_P_inst0_in;
wire [7:0] reg_P_inst0_out;
assign Mux2xBits8_inst0_I0 = enable_mux_O;
assign Mux2xBits8_inst0_I1 = const_222_8_out;
assign Mux2xBits8_inst0_S = RESET;
Mux2xBits8 Mux2xBits8_inst0 (
    .I0(Mux2xBits8_inst0_I0),
    .I1(Mux2xBits8_inst0_I1),
    .S(Mux2xBits8_inst0_S),
    .O(Mux2xBits8_inst0_O)
);
coreir_const #(
    .value(8'hde),
    .width(8)
) const_222_8 (
    .out(const_222_8_out)
);
assign enable_mux_I0 = reg_P_inst0_out;
assign enable_mux_I1 = I;
assign enable_mux_S = CE;
Mux2xBits8 enable_mux (
    .I0(enable_mux_I0),
    .I1(enable_mux_I1),
    .S(enable_mux_S),
    .O(enable_mux_O)
);
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = Mux2xBits8_inst0_O;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O = reg_P_inst0_out;
endmodule

module test_enable_reg (
    input [7:0] I,
    output [7:0] O,
    input CLK,
    input CE,
    input RESET
);
wire [7:0] Register_inst0_I;
wire [7:0] Register_inst0_O;
wire Register_inst0_CLK;
wire Register_inst0_CE;
wire Register_inst0_RESET;
assign Register_inst0_I = I;
assign Register_inst0_CLK = CLK;
assign Register_inst0_CE = CE;
assign Register_inst0_RESET = RESET;
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(Register_inst0_CLK),
    .CE(Register_inst0_CE),
    .RESET(Register_inst0_RESET)
);
assign O = Register_inst0_O;
endmodule

