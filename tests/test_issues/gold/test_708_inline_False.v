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

module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module commonlib_muxn__N2__width8 (
    input [7:0] in_data_0,
    input [7:0] in_data_1,
    input [0:0] in_sel,
    output [7:0] out
);
wire [7:0] _join_in0;
wire [7:0] _join_in1;
wire _join_sel;
wire [7:0] _join_out;
assign _join_in0 = in_data_0;
assign _join_in1 = in_data_1;
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

module Mux2xTuplex_OutUInt8 (
    input [7:0] I0_x,
    input [7:0] I1_x,
    output [7:0] O_x,
    input S
);
wire [7:0] coreir_commonlib_mux2x8_inst0_in_data_0;
wire [7:0] coreir_commonlib_mux2x8_inst0_in_data_1;
wire [0:0] coreir_commonlib_mux2x8_inst0_in_sel;
wire [7:0] coreir_commonlib_mux2x8_inst0_out;
assign coreir_commonlib_mux2x8_inst0_in_data_0 = I0_x;
assign coreir_commonlib_mux2x8_inst0_in_data_1 = I1_x;
assign coreir_commonlib_mux2x8_inst0_in_sel[0] = S;
commonlib_muxn__N2__width8 coreir_commonlib_mux2x8_inst0 (
    .in_data_0(coreir_commonlib_mux2x8_inst0_in_data_0),
    .in_data_1(coreir_commonlib_mux2x8_inst0_in_data_1),
    .in_sel(coreir_commonlib_mux2x8_inst0_in_sel),
    .out(coreir_commonlib_mux2x8_inst0_out)
);
assign O_x = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Test_comb (
    output [7:0] O0_x,
    output [7:0] O1_a_x,
    input c,
    input [7:0] self_a_O_x
);
wire [7:0] Mux2xTuplex_OutUInt8_inst0_I0_x;
wire [7:0] Mux2xTuplex_OutUInt8_inst0_I1_x;
wire [7:0] Mux2xTuplex_OutUInt8_inst0_O_x;
wire Mux2xTuplex_OutUInt8_inst0_S;
wire [7:0] const_1_8_out;
wire [7:0] magma_Bits_8_add_inst0_in0;
wire [7:0] magma_Bits_8_add_inst0_in1;
wire [7:0] magma_Bits_8_add_inst0_out;
assign Mux2xTuplex_OutUInt8_inst0_I0_x = self_a_O_x;
assign Mux2xTuplex_OutUInt8_inst0_I1_x = magma_Bits_8_add_inst0_out;
assign Mux2xTuplex_OutUInt8_inst0_S = c;
Mux2xTuplex_OutUInt8 Mux2xTuplex_OutUInt8_inst0 (
    .I0_x(Mux2xTuplex_OutUInt8_inst0_I0_x),
    .I1_x(Mux2xTuplex_OutUInt8_inst0_I1_x),
    .O_x(Mux2xTuplex_OutUInt8_inst0_O_x),
    .S(Mux2xTuplex_OutUInt8_inst0_S)
);
coreir_const #(
    .value(8'h01),
    .width(8)
) const_1_8 (
    .out(const_1_8_out)
);
assign magma_Bits_8_add_inst0_in0 = self_a_O_x;
assign magma_Bits_8_add_inst0_in1 = const_1_8_out;
coreir_add #(
    .width(8)
) magma_Bits_8_add_inst0 (
    .in0(magma_Bits_8_add_inst0_in0),
    .in1(magma_Bits_8_add_inst0_in1),
    .out(magma_Bits_8_add_inst0_out)
);
assign O0_x = self_a_O_x;
assign O1_a_x = Mux2xTuplex_OutUInt8_inst0_O_x;
endmodule

module Test (
    input CLK,
    output [7:0] O_a_x,
    input c
);
wire [7:0] Test_comb_inst0_O0_x;
wire [7:0] Test_comb_inst0_O1_a_x;
wire Test_comb_inst0_c;
wire [7:0] Test_comb_inst0_self_a_O_x;
wire reg_P_inst0_clk;
wire [7:0] reg_P_inst0_in;
wire [7:0] reg_P_inst0_out;
assign Test_comb_inst0_c = c;
assign Test_comb_inst0_self_a_O_x = reg_P_inst0_out;
Test_comb Test_comb_inst0 (
    .O0_x(Test_comb_inst0_O0_x),
    .O1_a_x(Test_comb_inst0_O1_a_x),
    .c(Test_comb_inst0_c),
    .self_a_O_x(Test_comb_inst0_self_a_O_x)
);
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = Test_comb_inst0_O0_x;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(8'h00),
    .width(8)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O_a_x = Test_comb_inst0_O1_a_x;
endmodule

