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

module coreir_eq #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 == in1;
endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module corebit_xor (
    input in0,
    input in1,
    output out
);
  assign out = in0 ^ in1;
endmodule

module corebit_not (
    input in,
    output out
);
  assign out = ~in;
endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module corebit_and (
    input in0,
    input in1,
    output out
);
  assign out = in0 & in1;
endmodule

module commonlib_muxn__N2__width4 (
    input [3:0] in_data [1:0],
    input [0:0] in_sel,
    output [3:0] out
);
wire [3:0] _join_in0;
wire [3:0] _join_in1;
wire _join_sel;
wire [3:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(4)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module commonlib_muxn__N2__width1 (
    input [0:0] in_data [1:0],
    input [0:0] in_sel,
    output [0:0] out
);
wire [0:0] _join_in0;
wire [0:0] _join_in1;
wire _join_sel;
wire [0:0] _join_out;
assign _join_in0 = in_data[0];
assign _join_in1 = in_data[1];
assign _join_sel = in_sel[0];
coreir_mux #(
    .width(1)
) _join (
    .in0(_join_in0),
    .in1(_join_in1),
    .sel(_join_sel),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xOutBits4 (
    input [3:0] I0,
    input [3:0] I1,
    input S,
    output [3:0] O
);
wire [3:0] coreir_commonlib_mux2x4_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x4_inst0_in_sel;
wire [3:0] coreir_commonlib_mux2x4_inst0_out;
assign coreir_commonlib_mux2x4_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x4_inst0_in_data[0] = I0;
assign coreir_commonlib_mux2x4_inst0_in_sel[0] = S;
commonlib_muxn__N2__width4 coreir_commonlib_mux2x4_inst0 (
    .in_data(coreir_commonlib_mux2x4_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x4_inst0_in_sel),
    .out(coreir_commonlib_mux2x4_inst0_out)
);
assign O = coreir_commonlib_mux2x4_inst0_out;
endmodule

module Register_comb (
    input [3:0] value,
    input en,
    input [3:0] self_value_O,
    output [3:0] O0,
    output [3:0] O1
);
wire [3:0] Mux2xOutBits4_inst0_I0;
wire [3:0] Mux2xOutBits4_inst0_I1;
wire Mux2xOutBits4_inst0_S;
wire [3:0] Mux2xOutBits4_inst0_O;
assign Mux2xOutBits4_inst0_I0 = self_value_O;
assign Mux2xOutBits4_inst0_I1 = value;
assign Mux2xOutBits4_inst0_S = en;
Mux2xOutBits4 Mux2xOutBits4_inst0 (
    .I0(Mux2xOutBits4_inst0_I0),
    .I1(Mux2xOutBits4_inst0_I1),
    .S(Mux2xOutBits4_inst0_S),
    .O(Mux2xOutBits4_inst0_O)
);
assign O0 = Mux2xOutBits4_inst0_O;
assign O1 = self_value_O;
endmodule

module Register (
    input [3:0] value,
    input en,
    input CLK,
    output [3:0] O
);
wire [3:0] Register_comb_inst0_value;
wire Register_comb_inst0_en;
wire [3:0] Register_comb_inst0_self_value_O;
wire [3:0] Register_comb_inst0_O0;
wire [3:0] Register_comb_inst0_O1;
wire reg_P_inst0_clk;
wire [3:0] reg_P_inst0_in;
wire [3:0] reg_P_inst0_out;
assign Register_comb_inst0_value = value;
assign Register_comb_inst0_en = en;
assign Register_comb_inst0_self_value_O = reg_P_inst0_out;
Register_comb Register_comb_inst0 (
    .value(Register_comb_inst0_value),
    .en(Register_comb_inst0_en),
    .self_value_O(Register_comb_inst0_self_value_O),
    .O0(Register_comb_inst0_O0),
    .O1(Register_comb_inst0_O1)
);
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = Register_comb_inst0_O0;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(4'h0),
    .width(4)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(reg_P_inst0_out)
);
assign O = Register_comb_inst0_O1;
endmodule

module Mux2xOutBit (
    input I0,
    input I1,
    input S,
    output O
);
wire [0:0] coreir_commonlib_mux2x1_inst0_in_data [1:0];
wire [0:0] coreir_commonlib_mux2x1_inst0_in_sel;
wire [0:0] coreir_commonlib_mux2x1_inst0_out;
assign coreir_commonlib_mux2x1_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x1_inst0_in_data[0] = I0;
assign coreir_commonlib_mux2x1_inst0_in_sel[0] = S;
commonlib_muxn__N2__width1 coreir_commonlib_mux2x1_inst0 (
    .in_data(coreir_commonlib_mux2x1_inst0_in_data),
    .in_sel(coreir_commonlib_mux2x1_inst0_in_sel),
    .out(coreir_commonlib_mux2x1_inst0_out)
);
assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module RegisterMode_comb (
    input [1:0] mode,
    input [3:0] const_,
    input [3:0] value,
    input clk_en,
    input config_we,
    input [3:0] config_data,
    input [3:0] self_register_O,
    output [3:0] O0,
    output O1,
    output [3:0] O2,
    output [3:0] O3
);
wire Mux2xOutBit_inst0_I0;
wire Mux2xOutBit_inst0_I1;
wire Mux2xOutBit_inst0_S;
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_I0;
wire Mux2xOutBit_inst1_I1;
wire Mux2xOutBit_inst1_S;
wire Mux2xOutBit_inst1_O;
wire Mux2xOutBit_inst2_I0;
wire Mux2xOutBit_inst2_I1;
wire Mux2xOutBit_inst2_S;
wire Mux2xOutBit_inst2_O;
wire Mux2xOutBit_inst3_I0;
wire Mux2xOutBit_inst3_I1;
wire Mux2xOutBit_inst3_S;
wire Mux2xOutBit_inst3_O;
wire Mux2xOutBit_inst4_I0;
wire Mux2xOutBit_inst4_I1;
wire Mux2xOutBit_inst4_S;
wire Mux2xOutBit_inst4_O;
wire Mux2xOutBit_inst5_I0;
wire Mux2xOutBit_inst5_I1;
wire Mux2xOutBit_inst5_S;
wire Mux2xOutBit_inst5_O;
wire [3:0] Mux2xOutBits4_inst0_I0;
wire [3:0] Mux2xOutBits4_inst0_I1;
wire Mux2xOutBits4_inst0_S;
wire [3:0] Mux2xOutBits4_inst0_O;
wire [3:0] Mux2xOutBits4_inst1_I0;
wire [3:0] Mux2xOutBits4_inst1_I1;
wire Mux2xOutBits4_inst1_S;
wire [3:0] Mux2xOutBits4_inst1_O;
wire [3:0] Mux2xOutBits4_inst10_I0;
wire [3:0] Mux2xOutBits4_inst10_I1;
wire Mux2xOutBits4_inst10_S;
wire [3:0] Mux2xOutBits4_inst10_O;
wire [3:0] Mux2xOutBits4_inst11_I0;
wire [3:0] Mux2xOutBits4_inst11_I1;
wire Mux2xOutBits4_inst11_S;
wire [3:0] Mux2xOutBits4_inst11_O;
wire [3:0] Mux2xOutBits4_inst12_I0;
wire [3:0] Mux2xOutBits4_inst12_I1;
wire Mux2xOutBits4_inst12_S;
wire [3:0] Mux2xOutBits4_inst12_O;
wire [3:0] Mux2xOutBits4_inst13_I0;
wire [3:0] Mux2xOutBits4_inst13_I1;
wire Mux2xOutBits4_inst13_S;
wire [3:0] Mux2xOutBits4_inst13_O;
wire [3:0] Mux2xOutBits4_inst14_I0;
wire [3:0] Mux2xOutBits4_inst14_I1;
wire Mux2xOutBits4_inst14_S;
wire [3:0] Mux2xOutBits4_inst14_O;
wire [3:0] Mux2xOutBits4_inst2_I0;
wire [3:0] Mux2xOutBits4_inst2_I1;
wire Mux2xOutBits4_inst2_S;
wire [3:0] Mux2xOutBits4_inst2_O;
wire [3:0] Mux2xOutBits4_inst3_I0;
wire [3:0] Mux2xOutBits4_inst3_I1;
wire Mux2xOutBits4_inst3_S;
wire [3:0] Mux2xOutBits4_inst3_O;
wire [3:0] Mux2xOutBits4_inst4_I0;
wire [3:0] Mux2xOutBits4_inst4_I1;
wire Mux2xOutBits4_inst4_S;
wire [3:0] Mux2xOutBits4_inst4_O;
wire [3:0] Mux2xOutBits4_inst5_I0;
wire [3:0] Mux2xOutBits4_inst5_I1;
wire Mux2xOutBits4_inst5_S;
wire [3:0] Mux2xOutBits4_inst5_O;
wire [3:0] Mux2xOutBits4_inst6_I0;
wire [3:0] Mux2xOutBits4_inst6_I1;
wire Mux2xOutBits4_inst6_S;
wire [3:0] Mux2xOutBits4_inst6_O;
wire [3:0] Mux2xOutBits4_inst7_I0;
wire [3:0] Mux2xOutBits4_inst7_I1;
wire Mux2xOutBits4_inst7_S;
wire [3:0] Mux2xOutBits4_inst7_O;
wire [3:0] Mux2xOutBits4_inst8_I0;
wire [3:0] Mux2xOutBits4_inst8_I1;
wire Mux2xOutBits4_inst8_S;
wire [3:0] Mux2xOutBits4_inst8_O;
wire [3:0] Mux2xOutBits4_inst9_I0;
wire [3:0] Mux2xOutBits4_inst9_I1;
wire Mux2xOutBits4_inst9_S;
wire [3:0] Mux2xOutBits4_inst9_O;
wire bit_const_0_None_out;
wire bit_const_1_None_out;
wire [1:0] const_0_2_out;
wire [1:0] const_1_2_out;
wire magma_Bit_and_inst0_in0;
wire magma_Bit_and_inst0_in1;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_in0;
wire magma_Bit_and_inst1_in1;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst10_in0;
wire magma_Bit_and_inst10_in1;
wire magma_Bit_and_inst10_out;
wire magma_Bit_and_inst11_in0;
wire magma_Bit_and_inst11_in1;
wire magma_Bit_and_inst11_out;
wire magma_Bit_and_inst2_in0;
wire magma_Bit_and_inst2_in1;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst3_in0;
wire magma_Bit_and_inst3_in1;
wire magma_Bit_and_inst3_out;
wire magma_Bit_and_inst4_in0;
wire magma_Bit_and_inst4_in1;
wire magma_Bit_and_inst4_out;
wire magma_Bit_and_inst5_in0;
wire magma_Bit_and_inst5_in1;
wire magma_Bit_and_inst5_out;
wire magma_Bit_and_inst6_in0;
wire magma_Bit_and_inst6_in1;
wire magma_Bit_and_inst6_out;
wire magma_Bit_and_inst7_in0;
wire magma_Bit_and_inst7_in1;
wire magma_Bit_and_inst7_out;
wire magma_Bit_and_inst8_in0;
wire magma_Bit_and_inst8_in1;
wire magma_Bit_and_inst8_out;
wire magma_Bit_and_inst9_in0;
wire magma_Bit_and_inst9_in1;
wire magma_Bit_and_inst9_out;
wire magma_Bit_not_inst0_in;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_in;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst10_in;
wire magma_Bit_not_inst10_out;
wire magma_Bit_not_inst11_in;
wire magma_Bit_not_inst11_out;
wire magma_Bit_not_inst12_in;
wire magma_Bit_not_inst12_out;
wire magma_Bit_not_inst13_in;
wire magma_Bit_not_inst13_out;
wire magma_Bit_not_inst14_in;
wire magma_Bit_not_inst14_out;
wire magma_Bit_not_inst15_in;
wire magma_Bit_not_inst15_out;
wire magma_Bit_not_inst16_in;
wire magma_Bit_not_inst16_out;
wire magma_Bit_not_inst17_in;
wire magma_Bit_not_inst17_out;
wire magma_Bit_not_inst18_in;
wire magma_Bit_not_inst18_out;
wire magma_Bit_not_inst19_in;
wire magma_Bit_not_inst19_out;
wire magma_Bit_not_inst2_in;
wire magma_Bit_not_inst2_out;
wire magma_Bit_not_inst20_in;
wire magma_Bit_not_inst20_out;
wire magma_Bit_not_inst21_in;
wire magma_Bit_not_inst21_out;
wire magma_Bit_not_inst22_in;
wire magma_Bit_not_inst22_out;
wire magma_Bit_not_inst23_in;
wire magma_Bit_not_inst23_out;
wire magma_Bit_not_inst24_in;
wire magma_Bit_not_inst24_out;
wire magma_Bit_not_inst25_in;
wire magma_Bit_not_inst25_out;
wire magma_Bit_not_inst26_in;
wire magma_Bit_not_inst26_out;
wire magma_Bit_not_inst3_in;
wire magma_Bit_not_inst3_out;
wire magma_Bit_not_inst4_in;
wire magma_Bit_not_inst4_out;
wire magma_Bit_not_inst5_in;
wire magma_Bit_not_inst5_out;
wire magma_Bit_not_inst6_in;
wire magma_Bit_not_inst6_out;
wire magma_Bit_not_inst7_in;
wire magma_Bit_not_inst7_out;
wire magma_Bit_not_inst8_in;
wire magma_Bit_not_inst8_out;
wire magma_Bit_not_inst9_in;
wire magma_Bit_not_inst9_out;
wire magma_Bit_xor_inst0_in0;
wire magma_Bit_xor_inst0_in1;
wire magma_Bit_xor_inst0_out;
wire magma_Bit_xor_inst1_in0;
wire magma_Bit_xor_inst1_in1;
wire magma_Bit_xor_inst1_out;
wire magma_Bit_xor_inst10_in0;
wire magma_Bit_xor_inst10_in1;
wire magma_Bit_xor_inst10_out;
wire magma_Bit_xor_inst11_in0;
wire magma_Bit_xor_inst11_in1;
wire magma_Bit_xor_inst11_out;
wire magma_Bit_xor_inst12_in0;
wire magma_Bit_xor_inst12_in1;
wire magma_Bit_xor_inst12_out;
wire magma_Bit_xor_inst13_in0;
wire magma_Bit_xor_inst13_in1;
wire magma_Bit_xor_inst13_out;
wire magma_Bit_xor_inst14_in0;
wire magma_Bit_xor_inst14_in1;
wire magma_Bit_xor_inst14_out;
wire magma_Bit_xor_inst2_in0;
wire magma_Bit_xor_inst2_in1;
wire magma_Bit_xor_inst2_out;
wire magma_Bit_xor_inst3_in0;
wire magma_Bit_xor_inst3_in1;
wire magma_Bit_xor_inst3_out;
wire magma_Bit_xor_inst4_in0;
wire magma_Bit_xor_inst4_in1;
wire magma_Bit_xor_inst4_out;
wire magma_Bit_xor_inst5_in0;
wire magma_Bit_xor_inst5_in1;
wire magma_Bit_xor_inst5_out;
wire magma_Bit_xor_inst6_in0;
wire magma_Bit_xor_inst6_in1;
wire magma_Bit_xor_inst6_out;
wire magma_Bit_xor_inst7_in0;
wire magma_Bit_xor_inst7_in1;
wire magma_Bit_xor_inst7_out;
wire magma_Bit_xor_inst8_in0;
wire magma_Bit_xor_inst8_in1;
wire magma_Bit_xor_inst8_out;
wire magma_Bit_xor_inst9_in0;
wire magma_Bit_xor_inst9_in1;
wire magma_Bit_xor_inst9_out;
wire [1:0] magma_Bits_2_eq_inst0_in0;
wire [1:0] magma_Bits_2_eq_inst0_in1;
wire magma_Bits_2_eq_inst0_out;
wire [1:0] magma_Bits_2_eq_inst1_in0;
wire [1:0] magma_Bits_2_eq_inst1_in1;
wire magma_Bits_2_eq_inst1_out;
wire [1:0] magma_Bits_2_eq_inst10_in0;
wire [1:0] magma_Bits_2_eq_inst10_in1;
wire magma_Bits_2_eq_inst10_out;
wire [1:0] magma_Bits_2_eq_inst11_in0;
wire [1:0] magma_Bits_2_eq_inst11_in1;
wire magma_Bits_2_eq_inst11_out;
wire [1:0] magma_Bits_2_eq_inst12_in0;
wire [1:0] magma_Bits_2_eq_inst12_in1;
wire magma_Bits_2_eq_inst12_out;
wire [1:0] magma_Bits_2_eq_inst13_in0;
wire [1:0] magma_Bits_2_eq_inst13_in1;
wire magma_Bits_2_eq_inst13_out;
wire [1:0] magma_Bits_2_eq_inst14_in0;
wire [1:0] magma_Bits_2_eq_inst14_in1;
wire magma_Bits_2_eq_inst14_out;
wire [1:0] magma_Bits_2_eq_inst15_in0;
wire [1:0] magma_Bits_2_eq_inst15_in1;
wire magma_Bits_2_eq_inst15_out;
wire [1:0] magma_Bits_2_eq_inst16_in0;
wire [1:0] magma_Bits_2_eq_inst16_in1;
wire magma_Bits_2_eq_inst16_out;
wire [1:0] magma_Bits_2_eq_inst17_in0;
wire [1:0] magma_Bits_2_eq_inst17_in1;
wire magma_Bits_2_eq_inst17_out;
wire [1:0] magma_Bits_2_eq_inst2_in0;
wire [1:0] magma_Bits_2_eq_inst2_in1;
wire magma_Bits_2_eq_inst2_out;
wire [1:0] magma_Bits_2_eq_inst3_in0;
wire [1:0] magma_Bits_2_eq_inst3_in1;
wire magma_Bits_2_eq_inst3_out;
wire [1:0] magma_Bits_2_eq_inst4_in0;
wire [1:0] magma_Bits_2_eq_inst4_in1;
wire magma_Bits_2_eq_inst4_out;
wire [1:0] magma_Bits_2_eq_inst5_in0;
wire [1:0] magma_Bits_2_eq_inst5_in1;
wire magma_Bits_2_eq_inst5_out;
wire [1:0] magma_Bits_2_eq_inst6_in0;
wire [1:0] magma_Bits_2_eq_inst6_in1;
wire magma_Bits_2_eq_inst6_out;
wire [1:0] magma_Bits_2_eq_inst7_in0;
wire [1:0] magma_Bits_2_eq_inst7_in1;
wire magma_Bits_2_eq_inst7_out;
wire [1:0] magma_Bits_2_eq_inst8_in0;
wire [1:0] magma_Bits_2_eq_inst8_in1;
wire magma_Bits_2_eq_inst8_out;
wire [1:0] magma_Bits_2_eq_inst9_in0;
wire [1:0] magma_Bits_2_eq_inst9_in1;
wire magma_Bits_2_eq_inst9_out;
assign Mux2xOutBit_inst0_I0 = clk_en;
assign Mux2xOutBit_inst0_I1 = bit_const_0_None_out;
assign Mux2xOutBit_inst0_S = magma_Bits_2_eq_inst1_out;
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(Mux2xOutBit_inst0_I0),
    .I1(Mux2xOutBit_inst0_I1),
    .S(Mux2xOutBit_inst0_S),
    .O(Mux2xOutBit_inst0_O)
);
assign Mux2xOutBit_inst1_I0 = Mux2xOutBit_inst0_O;
assign Mux2xOutBit_inst1_I1 = bit_const_0_None_out;
assign Mux2xOutBit_inst1_S = magma_Bits_2_eq_inst4_out;
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(Mux2xOutBit_inst1_I0),
    .I1(Mux2xOutBit_inst1_I1),
    .S(Mux2xOutBit_inst1_S),
    .O(Mux2xOutBit_inst1_O)
);
assign Mux2xOutBit_inst2_I0 = Mux2xOutBit_inst1_O;
assign Mux2xOutBit_inst2_I1 = bit_const_1_None_out;
assign Mux2xOutBit_inst2_S = magma_Bit_not_inst1_out;
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(Mux2xOutBit_inst2_I0),
    .I1(Mux2xOutBit_inst2_I1),
    .S(Mux2xOutBit_inst2_S),
    .O(Mux2xOutBit_inst2_O)
);
assign Mux2xOutBit_inst3_I0 = clk_en;
assign Mux2xOutBit_inst3_I1 = bit_const_0_None_out;
assign Mux2xOutBit_inst3_S = magma_Bit_and_inst3_out;
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(Mux2xOutBit_inst3_I0),
    .I1(Mux2xOutBit_inst3_I1),
    .S(Mux2xOutBit_inst3_S),
    .O(Mux2xOutBit_inst3_O)
);
assign Mux2xOutBit_inst4_I0 = Mux2xOutBit_inst3_O;
assign Mux2xOutBit_inst4_I1 = bit_const_0_None_out;
assign Mux2xOutBit_inst4_S = magma_Bit_and_inst9_out;
Mux2xOutBit Mux2xOutBit_inst4 (
    .I0(Mux2xOutBit_inst4_I0),
    .I1(Mux2xOutBit_inst4_I1),
    .S(Mux2xOutBit_inst4_S),
    .O(Mux2xOutBit_inst4_O)
);
assign Mux2xOutBit_inst5_I0 = Mux2xOutBit_inst4_O;
assign Mux2xOutBit_inst5_I1 = bit_const_1_None_out;
assign Mux2xOutBit_inst5_S = magma_Bit_not_inst24_out;
Mux2xOutBit Mux2xOutBit_inst5 (
    .I0(Mux2xOutBit_inst5_I0),
    .I1(Mux2xOutBit_inst5_I1),
    .S(Mux2xOutBit_inst5_S),
    .O(Mux2xOutBit_inst5_O)
);
assign Mux2xOutBits4_inst0_I0 = value;
assign Mux2xOutBits4_inst0_I1 = value;
assign Mux2xOutBits4_inst0_S = magma_Bits_2_eq_inst0_out;
Mux2xOutBits4 Mux2xOutBits4_inst0 (
    .I0(Mux2xOutBits4_inst0_I0),
    .I1(Mux2xOutBits4_inst0_I1),
    .S(Mux2xOutBits4_inst0_S),
    .O(Mux2xOutBits4_inst0_O)
);
assign Mux2xOutBits4_inst1_I0 = self_register_O;
assign Mux2xOutBits4_inst1_I1 = self_register_O;
assign Mux2xOutBits4_inst1_S = magma_Bits_2_eq_inst2_out;
Mux2xOutBits4 Mux2xOutBits4_inst1 (
    .I0(Mux2xOutBits4_inst1_I0),
    .I1(Mux2xOutBits4_inst1_I1),
    .S(Mux2xOutBits4_inst1_S),
    .O(Mux2xOutBits4_inst1_O)
);
assign Mux2xOutBits4_inst10_I0 = Mux2xOutBits4_inst7_O;
assign Mux2xOutBits4_inst10_I1 = const_;
assign Mux2xOutBits4_inst10_S = magma_Bit_and_inst10_out;
Mux2xOutBits4 Mux2xOutBits4_inst10 (
    .I0(Mux2xOutBits4_inst10_I0),
    .I1(Mux2xOutBits4_inst10_I1),
    .S(Mux2xOutBits4_inst10_S),
    .O(Mux2xOutBits4_inst10_O)
);
assign Mux2xOutBits4_inst11_I0 = Mux2xOutBits4_inst8_O;
assign Mux2xOutBits4_inst11_I1 = self_register_O;
assign Mux2xOutBits4_inst11_S = magma_Bit_and_inst11_out;
Mux2xOutBits4 Mux2xOutBits4_inst11 (
    .I0(Mux2xOutBits4_inst11_I0),
    .I1(Mux2xOutBits4_inst11_I1),
    .S(Mux2xOutBits4_inst11_S),
    .O(Mux2xOutBits4_inst11_O)
);
assign Mux2xOutBits4_inst12_I0 = Mux2xOutBits4_inst9_O;
assign Mux2xOutBits4_inst12_I1 = config_data;
assign Mux2xOutBits4_inst12_S = magma_Bit_not_inst23_out;
Mux2xOutBits4 Mux2xOutBits4_inst12 (
    .I0(Mux2xOutBits4_inst12_I0),
    .I1(Mux2xOutBits4_inst12_I1),
    .S(Mux2xOutBits4_inst12_S),
    .O(Mux2xOutBits4_inst12_O)
);
assign Mux2xOutBits4_inst13_I0 = Mux2xOutBits4_inst10_O;
assign Mux2xOutBits4_inst13_I1 = self_register_O;
assign Mux2xOutBits4_inst13_S = magma_Bit_not_inst25_out;
Mux2xOutBits4 Mux2xOutBits4_inst13 (
    .I0(Mux2xOutBits4_inst13_I0),
    .I1(Mux2xOutBits4_inst13_I1),
    .S(Mux2xOutBits4_inst13_S),
    .O(Mux2xOutBits4_inst13_O)
);
assign Mux2xOutBits4_inst14_I0 = Mux2xOutBits4_inst11_O;
assign Mux2xOutBits4_inst14_I1 = self_register_O;
assign Mux2xOutBits4_inst14_S = magma_Bit_not_inst26_out;
Mux2xOutBits4 Mux2xOutBits4_inst14 (
    .I0(Mux2xOutBits4_inst14_I0),
    .I1(Mux2xOutBits4_inst14_I1),
    .S(Mux2xOutBits4_inst14_S),
    .O(Mux2xOutBits4_inst14_O)
);
assign Mux2xOutBits4_inst2_I0 = Mux2xOutBits4_inst0_O;
assign Mux2xOutBits4_inst2_I1 = value;
assign Mux2xOutBits4_inst2_S = magma_Bits_2_eq_inst3_out;
Mux2xOutBits4 Mux2xOutBits4_inst2 (
    .I0(Mux2xOutBits4_inst2_I0),
    .I1(Mux2xOutBits4_inst2_I1),
    .S(Mux2xOutBits4_inst2_S),
    .O(Mux2xOutBits4_inst2_O)
);
assign Mux2xOutBits4_inst3_I0 = Mux2xOutBits4_inst1_O;
assign Mux2xOutBits4_inst3_I1 = self_register_O;
assign Mux2xOutBits4_inst3_S = magma_Bits_2_eq_inst5_out;
Mux2xOutBits4 Mux2xOutBits4_inst3 (
    .I0(Mux2xOutBits4_inst3_I0),
    .I1(Mux2xOutBits4_inst3_I1),
    .S(Mux2xOutBits4_inst3_S),
    .O(Mux2xOutBits4_inst3_O)
);
assign Mux2xOutBits4_inst4_I0 = Mux2xOutBits4_inst2_O;
assign Mux2xOutBits4_inst4_I1 = config_data;
assign Mux2xOutBits4_inst4_S = magma_Bit_not_inst0_out;
Mux2xOutBits4 Mux2xOutBits4_inst4 (
    .I0(Mux2xOutBits4_inst4_I0),
    .I1(Mux2xOutBits4_inst4_I1),
    .S(Mux2xOutBits4_inst4_S),
    .O(Mux2xOutBits4_inst4_O)
);
assign Mux2xOutBits4_inst5_I0 = Mux2xOutBits4_inst3_O;
assign Mux2xOutBits4_inst5_I1 = self_register_O;
assign Mux2xOutBits4_inst5_S = magma_Bit_not_inst2_out;
Mux2xOutBits4 Mux2xOutBits4_inst5 (
    .I0(Mux2xOutBits4_inst5_I0),
    .I1(Mux2xOutBits4_inst5_I1),
    .S(Mux2xOutBits4_inst5_S),
    .O(Mux2xOutBits4_inst5_O)
);
assign Mux2xOutBits4_inst6_I0 = value;
assign Mux2xOutBits4_inst6_I1 = value;
assign Mux2xOutBits4_inst6_S = magma_Bit_and_inst1_out;
Mux2xOutBits4 Mux2xOutBits4_inst6 (
    .I0(Mux2xOutBits4_inst6_I0),
    .I1(Mux2xOutBits4_inst6_I1),
    .S(Mux2xOutBits4_inst6_S),
    .O(Mux2xOutBits4_inst6_O)
);
assign Mux2xOutBits4_inst7_I0 = self_register_O;
assign Mux2xOutBits4_inst7_I1 = value;
assign Mux2xOutBits4_inst7_S = magma_Bit_and_inst5_out;
Mux2xOutBits4 Mux2xOutBits4_inst7 (
    .I0(Mux2xOutBits4_inst7_I0),
    .I1(Mux2xOutBits4_inst7_I1),
    .S(Mux2xOutBits4_inst7_S),
    .O(Mux2xOutBits4_inst7_O)
);
assign Mux2xOutBits4_inst8_I0 = self_register_O;
assign Mux2xOutBits4_inst8_I1 = self_register_O;
assign Mux2xOutBits4_inst8_S = magma_Bit_and_inst7_out;
Mux2xOutBits4 Mux2xOutBits4_inst8 (
    .I0(Mux2xOutBits4_inst8_I0),
    .I1(Mux2xOutBits4_inst8_I1),
    .S(Mux2xOutBits4_inst8_S),
    .O(Mux2xOutBits4_inst8_O)
);
assign Mux2xOutBits4_inst9_I0 = Mux2xOutBits4_inst6_O;
assign Mux2xOutBits4_inst9_I1 = value;
assign Mux2xOutBits4_inst9_S = magma_Bit_and_inst8_out;
Mux2xOutBits4 Mux2xOutBits4_inst9 (
    .I0(Mux2xOutBits4_inst9_I0),
    .I1(Mux2xOutBits4_inst9_I1),
    .S(Mux2xOutBits4_inst9_S),
    .O(Mux2xOutBits4_inst9_O)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
corebit_const #(
    .value(1'b1)
) bit_const_1_None (
    .out(bit_const_1_None_out)
);
coreir_const #(
    .value(2'h0),
    .width(2)
) const_0_2 (
    .out(const_0_2_out)
);
coreir_const #(
    .value(2'h1),
    .width(2)
) const_1_2 (
    .out(const_1_2_out)
);
assign magma_Bit_and_inst0_in0 = magma_Bits_2_eq_inst6_out;
assign magma_Bit_and_inst0_in1 = magma_Bit_not_inst4_out;
corebit_and magma_Bit_and_inst0 (
    .in0(magma_Bit_and_inst0_in0),
    .in1(magma_Bit_and_inst0_in1),
    .out(magma_Bit_and_inst0_out)
);
assign magma_Bit_and_inst1_in0 = magma_Bit_and_inst0_out;
assign magma_Bit_and_inst1_in1 = magma_Bit_not_inst5_out;
corebit_and magma_Bit_and_inst1 (
    .in0(magma_Bit_and_inst1_in0),
    .in1(magma_Bit_and_inst1_in1),
    .out(magma_Bit_and_inst1_out)
);
assign magma_Bit_and_inst10_in0 = magma_Bits_2_eq_inst16_out;
assign magma_Bit_and_inst10_in1 = magma_Bit_not_inst20_out;
corebit_and magma_Bit_and_inst10 (
    .in0(magma_Bit_and_inst10_in0),
    .in1(magma_Bit_and_inst10_in1),
    .out(magma_Bit_and_inst10_out)
);
assign magma_Bit_and_inst11_in0 = magma_Bits_2_eq_inst17_out;
assign magma_Bit_and_inst11_in1 = magma_Bit_not_inst22_out;
corebit_and magma_Bit_and_inst11 (
    .in0(magma_Bit_and_inst11_in0),
    .in1(magma_Bit_and_inst11_in1),
    .out(magma_Bit_and_inst11_out)
);
assign magma_Bit_and_inst2_in0 = magma_Bits_2_eq_inst8_out;
assign magma_Bit_and_inst2_in1 = magma_Bit_not_inst7_out;
corebit_and magma_Bit_and_inst2 (
    .in0(magma_Bit_and_inst2_in0),
    .in1(magma_Bit_and_inst2_in1),
    .out(magma_Bit_and_inst2_out)
);
assign magma_Bit_and_inst3_in0 = magma_Bit_and_inst2_out;
assign magma_Bit_and_inst3_in1 = magma_Bit_not_inst8_out;
corebit_and magma_Bit_and_inst3 (
    .in0(magma_Bit_and_inst3_in0),
    .in1(magma_Bit_and_inst3_in1),
    .out(magma_Bit_and_inst3_out)
);
assign magma_Bit_and_inst4_in0 = magma_Bits_2_eq_inst10_out;
assign magma_Bit_and_inst4_in1 = magma_Bit_not_inst10_out;
corebit_and magma_Bit_and_inst4 (
    .in0(magma_Bit_and_inst4_in0),
    .in1(magma_Bit_and_inst4_in1),
    .out(magma_Bit_and_inst4_out)
);
assign magma_Bit_and_inst5_in0 = magma_Bit_and_inst4_out;
assign magma_Bit_and_inst5_in1 = magma_Bit_not_inst11_out;
corebit_and magma_Bit_and_inst5 (
    .in0(magma_Bit_and_inst5_in0),
    .in1(magma_Bit_and_inst5_in1),
    .out(magma_Bit_and_inst5_out)
);
assign magma_Bit_and_inst6_in0 = magma_Bits_2_eq_inst12_out;
assign magma_Bit_and_inst6_in1 = magma_Bit_not_inst13_out;
corebit_and magma_Bit_and_inst6 (
    .in0(magma_Bit_and_inst6_in0),
    .in1(magma_Bit_and_inst6_in1),
    .out(magma_Bit_and_inst6_out)
);
assign magma_Bit_and_inst7_in0 = magma_Bit_and_inst6_out;
assign magma_Bit_and_inst7_in1 = magma_Bit_not_inst14_out;
corebit_and magma_Bit_and_inst7 (
    .in0(magma_Bit_and_inst7_in0),
    .in1(magma_Bit_and_inst7_in1),
    .out(magma_Bit_and_inst7_out)
);
assign magma_Bit_and_inst8_in0 = magma_Bits_2_eq_inst14_out;
assign magma_Bit_and_inst8_in1 = magma_Bit_not_inst16_out;
corebit_and magma_Bit_and_inst8 (
    .in0(magma_Bit_and_inst8_in0),
    .in1(magma_Bit_and_inst8_in1),
    .out(magma_Bit_and_inst8_out)
);
assign magma_Bit_and_inst9_in0 = magma_Bits_2_eq_inst15_out;
assign magma_Bit_and_inst9_in1 = magma_Bit_not_inst18_out;
corebit_and magma_Bit_and_inst9 (
    .in0(magma_Bit_and_inst9_in0),
    .in1(magma_Bit_and_inst9_in1),
    .out(magma_Bit_and_inst9_out)
);
assign magma_Bit_not_inst0_in = magma_Bit_xor_inst0_out;
corebit_not magma_Bit_not_inst0 (
    .in(magma_Bit_not_inst0_in),
    .out(magma_Bit_not_inst0_out)
);
assign magma_Bit_not_inst1_in = magma_Bit_xor_inst1_out;
corebit_not magma_Bit_not_inst1 (
    .in(magma_Bit_not_inst1_in),
    .out(magma_Bit_not_inst1_out)
);
assign magma_Bit_not_inst10_in = magma_Bit_not_inst9_out;
corebit_not magma_Bit_not_inst10 (
    .in(magma_Bit_not_inst10_in),
    .out(magma_Bit_not_inst10_out)
);
assign magma_Bit_not_inst11_in = magma_Bits_2_eq_inst11_out;
corebit_not magma_Bit_not_inst11 (
    .in(magma_Bit_not_inst11_in),
    .out(magma_Bit_not_inst11_out)
);
assign magma_Bit_not_inst12_in = magma_Bit_xor_inst6_out;
corebit_not magma_Bit_not_inst12 (
    .in(magma_Bit_not_inst12_in),
    .out(magma_Bit_not_inst12_out)
);
assign magma_Bit_not_inst13_in = magma_Bit_not_inst12_out;
corebit_not magma_Bit_not_inst13 (
    .in(magma_Bit_not_inst13_in),
    .out(magma_Bit_not_inst13_out)
);
assign magma_Bit_not_inst14_in = magma_Bits_2_eq_inst13_out;
corebit_not magma_Bit_not_inst14 (
    .in(magma_Bit_not_inst14_in),
    .out(magma_Bit_not_inst14_out)
);
assign magma_Bit_not_inst15_in = magma_Bit_xor_inst7_out;
corebit_not magma_Bit_not_inst15 (
    .in(magma_Bit_not_inst15_in),
    .out(magma_Bit_not_inst15_out)
);
assign magma_Bit_not_inst16_in = magma_Bit_not_inst15_out;
corebit_not magma_Bit_not_inst16 (
    .in(magma_Bit_not_inst16_in),
    .out(magma_Bit_not_inst16_out)
);
assign magma_Bit_not_inst17_in = magma_Bit_xor_inst8_out;
corebit_not magma_Bit_not_inst17 (
    .in(magma_Bit_not_inst17_in),
    .out(magma_Bit_not_inst17_out)
);
assign magma_Bit_not_inst18_in = magma_Bit_not_inst17_out;
corebit_not magma_Bit_not_inst18 (
    .in(magma_Bit_not_inst18_in),
    .out(magma_Bit_not_inst18_out)
);
assign magma_Bit_not_inst19_in = magma_Bit_xor_inst9_out;
corebit_not magma_Bit_not_inst19 (
    .in(magma_Bit_not_inst19_in),
    .out(magma_Bit_not_inst19_out)
);
assign magma_Bit_not_inst2_in = magma_Bit_xor_inst2_out;
corebit_not magma_Bit_not_inst2 (
    .in(magma_Bit_not_inst2_in),
    .out(magma_Bit_not_inst2_out)
);
assign magma_Bit_not_inst20_in = magma_Bit_not_inst19_out;
corebit_not magma_Bit_not_inst20 (
    .in(magma_Bit_not_inst20_in),
    .out(magma_Bit_not_inst20_out)
);
assign magma_Bit_not_inst21_in = magma_Bit_xor_inst10_out;
corebit_not magma_Bit_not_inst21 (
    .in(magma_Bit_not_inst21_in),
    .out(magma_Bit_not_inst21_out)
);
assign magma_Bit_not_inst22_in = magma_Bit_not_inst21_out;
corebit_not magma_Bit_not_inst22 (
    .in(magma_Bit_not_inst22_in),
    .out(magma_Bit_not_inst22_out)
);
assign magma_Bit_not_inst23_in = magma_Bit_xor_inst11_out;
corebit_not magma_Bit_not_inst23 (
    .in(magma_Bit_not_inst23_in),
    .out(magma_Bit_not_inst23_out)
);
assign magma_Bit_not_inst24_in = magma_Bit_xor_inst12_out;
corebit_not magma_Bit_not_inst24 (
    .in(magma_Bit_not_inst24_in),
    .out(magma_Bit_not_inst24_out)
);
assign magma_Bit_not_inst25_in = magma_Bit_xor_inst13_out;
corebit_not magma_Bit_not_inst25 (
    .in(magma_Bit_not_inst25_in),
    .out(magma_Bit_not_inst25_out)
);
assign magma_Bit_not_inst26_in = magma_Bit_xor_inst14_out;
corebit_not magma_Bit_not_inst26 (
    .in(magma_Bit_not_inst26_in),
    .out(magma_Bit_not_inst26_out)
);
assign magma_Bit_not_inst3_in = magma_Bit_xor_inst3_out;
corebit_not magma_Bit_not_inst3 (
    .in(magma_Bit_not_inst3_in),
    .out(magma_Bit_not_inst3_out)
);
assign magma_Bit_not_inst4_in = magma_Bit_not_inst3_out;
corebit_not magma_Bit_not_inst4 (
    .in(magma_Bit_not_inst4_in),
    .out(magma_Bit_not_inst4_out)
);
assign magma_Bit_not_inst5_in = magma_Bits_2_eq_inst7_out;
corebit_not magma_Bit_not_inst5 (
    .in(magma_Bit_not_inst5_in),
    .out(magma_Bit_not_inst5_out)
);
assign magma_Bit_not_inst6_in = magma_Bit_xor_inst4_out;
corebit_not magma_Bit_not_inst6 (
    .in(magma_Bit_not_inst6_in),
    .out(magma_Bit_not_inst6_out)
);
assign magma_Bit_not_inst7_in = magma_Bit_not_inst6_out;
corebit_not magma_Bit_not_inst7 (
    .in(magma_Bit_not_inst7_in),
    .out(magma_Bit_not_inst7_out)
);
assign magma_Bit_not_inst8_in = magma_Bits_2_eq_inst9_out;
corebit_not magma_Bit_not_inst8 (
    .in(magma_Bit_not_inst8_in),
    .out(magma_Bit_not_inst8_out)
);
assign magma_Bit_not_inst9_in = magma_Bit_xor_inst5_out;
corebit_not magma_Bit_not_inst9 (
    .in(magma_Bit_not_inst9_in),
    .out(magma_Bit_not_inst9_out)
);
assign magma_Bit_xor_inst0_in0 = config_we;
assign magma_Bit_xor_inst0_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst0 (
    .in0(magma_Bit_xor_inst0_in0),
    .in1(magma_Bit_xor_inst0_in1),
    .out(magma_Bit_xor_inst0_out)
);
assign magma_Bit_xor_inst1_in0 = config_we;
assign magma_Bit_xor_inst1_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst1 (
    .in0(magma_Bit_xor_inst1_in0),
    .in1(magma_Bit_xor_inst1_in1),
    .out(magma_Bit_xor_inst1_out)
);
assign magma_Bit_xor_inst10_in0 = config_we;
assign magma_Bit_xor_inst10_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst10 (
    .in0(magma_Bit_xor_inst10_in0),
    .in1(magma_Bit_xor_inst10_in1),
    .out(magma_Bit_xor_inst10_out)
);
assign magma_Bit_xor_inst11_in0 = config_we;
assign magma_Bit_xor_inst11_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst11 (
    .in0(magma_Bit_xor_inst11_in0),
    .in1(magma_Bit_xor_inst11_in1),
    .out(magma_Bit_xor_inst11_out)
);
assign magma_Bit_xor_inst12_in0 = config_we;
assign magma_Bit_xor_inst12_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst12 (
    .in0(magma_Bit_xor_inst12_in0),
    .in1(magma_Bit_xor_inst12_in1),
    .out(magma_Bit_xor_inst12_out)
);
assign magma_Bit_xor_inst13_in0 = config_we;
assign magma_Bit_xor_inst13_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst13 (
    .in0(magma_Bit_xor_inst13_in0),
    .in1(magma_Bit_xor_inst13_in1),
    .out(magma_Bit_xor_inst13_out)
);
assign magma_Bit_xor_inst14_in0 = config_we;
assign magma_Bit_xor_inst14_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst14 (
    .in0(magma_Bit_xor_inst14_in0),
    .in1(magma_Bit_xor_inst14_in1),
    .out(magma_Bit_xor_inst14_out)
);
assign magma_Bit_xor_inst2_in0 = config_we;
assign magma_Bit_xor_inst2_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst2 (
    .in0(magma_Bit_xor_inst2_in0),
    .in1(magma_Bit_xor_inst2_in1),
    .out(magma_Bit_xor_inst2_out)
);
assign magma_Bit_xor_inst3_in0 = config_we;
assign magma_Bit_xor_inst3_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst3 (
    .in0(magma_Bit_xor_inst3_in0),
    .in1(magma_Bit_xor_inst3_in1),
    .out(magma_Bit_xor_inst3_out)
);
assign magma_Bit_xor_inst4_in0 = config_we;
assign magma_Bit_xor_inst4_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst4 (
    .in0(magma_Bit_xor_inst4_in0),
    .in1(magma_Bit_xor_inst4_in1),
    .out(magma_Bit_xor_inst4_out)
);
assign magma_Bit_xor_inst5_in0 = config_we;
assign magma_Bit_xor_inst5_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst5 (
    .in0(magma_Bit_xor_inst5_in0),
    .in1(magma_Bit_xor_inst5_in1),
    .out(magma_Bit_xor_inst5_out)
);
assign magma_Bit_xor_inst6_in0 = config_we;
assign magma_Bit_xor_inst6_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst6 (
    .in0(magma_Bit_xor_inst6_in0),
    .in1(magma_Bit_xor_inst6_in1),
    .out(magma_Bit_xor_inst6_out)
);
assign magma_Bit_xor_inst7_in0 = config_we;
assign magma_Bit_xor_inst7_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst7 (
    .in0(magma_Bit_xor_inst7_in0),
    .in1(magma_Bit_xor_inst7_in1),
    .out(magma_Bit_xor_inst7_out)
);
assign magma_Bit_xor_inst8_in0 = config_we;
assign magma_Bit_xor_inst8_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst8 (
    .in0(magma_Bit_xor_inst8_in0),
    .in1(magma_Bit_xor_inst8_in1),
    .out(magma_Bit_xor_inst8_out)
);
assign magma_Bit_xor_inst9_in0 = config_we;
assign magma_Bit_xor_inst9_in1 = bit_const_1_None_out;
corebit_xor magma_Bit_xor_inst9 (
    .in0(magma_Bit_xor_inst9_in0),
    .in1(magma_Bit_xor_inst9_in1),
    .out(magma_Bit_xor_inst9_out)
);
assign magma_Bits_2_eq_inst0_in0 = mode;
assign magma_Bits_2_eq_inst0_in1 = const_1_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst0 (
    .in0(magma_Bits_2_eq_inst0_in0),
    .in1(magma_Bits_2_eq_inst0_in1),
    .out(magma_Bits_2_eq_inst0_out)
);
assign magma_Bits_2_eq_inst1_in0 = mode;
assign magma_Bits_2_eq_inst1_in1 = const_1_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst1 (
    .in0(magma_Bits_2_eq_inst1_in0),
    .in1(magma_Bits_2_eq_inst1_in1),
    .out(magma_Bits_2_eq_inst1_out)
);
assign magma_Bits_2_eq_inst10_in0 = mode;
assign magma_Bits_2_eq_inst10_in1 = const_1_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst10 (
    .in0(magma_Bits_2_eq_inst10_in0),
    .in1(magma_Bits_2_eq_inst10_in1),
    .out(magma_Bits_2_eq_inst10_out)
);
assign magma_Bits_2_eq_inst11_in0 = mode;
assign magma_Bits_2_eq_inst11_in1 = const_0_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst11 (
    .in0(magma_Bits_2_eq_inst11_in0),
    .in1(magma_Bits_2_eq_inst11_in1),
    .out(magma_Bits_2_eq_inst11_out)
);
assign magma_Bits_2_eq_inst12_in0 = mode;
assign magma_Bits_2_eq_inst12_in1 = const_1_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst12 (
    .in0(magma_Bits_2_eq_inst12_in0),
    .in1(magma_Bits_2_eq_inst12_in1),
    .out(magma_Bits_2_eq_inst12_out)
);
assign magma_Bits_2_eq_inst13_in0 = mode;
assign magma_Bits_2_eq_inst13_in1 = const_0_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst13 (
    .in0(magma_Bits_2_eq_inst13_in0),
    .in1(magma_Bits_2_eq_inst13_in1),
    .out(magma_Bits_2_eq_inst13_out)
);
assign magma_Bits_2_eq_inst14_in0 = mode;
assign magma_Bits_2_eq_inst14_in1 = const_0_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst14 (
    .in0(magma_Bits_2_eq_inst14_in0),
    .in1(magma_Bits_2_eq_inst14_in1),
    .out(magma_Bits_2_eq_inst14_out)
);
assign magma_Bits_2_eq_inst15_in0 = mode;
assign magma_Bits_2_eq_inst15_in1 = const_0_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst15 (
    .in0(magma_Bits_2_eq_inst15_in0),
    .in1(magma_Bits_2_eq_inst15_in1),
    .out(magma_Bits_2_eq_inst15_out)
);
assign magma_Bits_2_eq_inst16_in0 = mode;
assign magma_Bits_2_eq_inst16_in1 = const_0_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst16 (
    .in0(magma_Bits_2_eq_inst16_in0),
    .in1(magma_Bits_2_eq_inst16_in1),
    .out(magma_Bits_2_eq_inst16_out)
);
assign magma_Bits_2_eq_inst17_in0 = mode;
assign magma_Bits_2_eq_inst17_in1 = const_0_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst17 (
    .in0(magma_Bits_2_eq_inst17_in0),
    .in1(magma_Bits_2_eq_inst17_in1),
    .out(magma_Bits_2_eq_inst17_out)
);
assign magma_Bits_2_eq_inst2_in0 = mode;
assign magma_Bits_2_eq_inst2_in1 = const_1_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst2 (
    .in0(magma_Bits_2_eq_inst2_in0),
    .in1(magma_Bits_2_eq_inst2_in1),
    .out(magma_Bits_2_eq_inst2_out)
);
assign magma_Bits_2_eq_inst3_in0 = mode;
assign magma_Bits_2_eq_inst3_in1 = const_0_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst3 (
    .in0(magma_Bits_2_eq_inst3_in0),
    .in1(magma_Bits_2_eq_inst3_in1),
    .out(magma_Bits_2_eq_inst3_out)
);
assign magma_Bits_2_eq_inst4_in0 = mode;
assign magma_Bits_2_eq_inst4_in1 = const_0_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst4 (
    .in0(magma_Bits_2_eq_inst4_in0),
    .in1(magma_Bits_2_eq_inst4_in1),
    .out(magma_Bits_2_eq_inst4_out)
);
assign magma_Bits_2_eq_inst5_in0 = mode;
assign magma_Bits_2_eq_inst5_in1 = const_0_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst5 (
    .in0(magma_Bits_2_eq_inst5_in0),
    .in1(magma_Bits_2_eq_inst5_in1),
    .out(magma_Bits_2_eq_inst5_out)
);
assign magma_Bits_2_eq_inst6_in0 = mode;
assign magma_Bits_2_eq_inst6_in1 = const_1_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst6 (
    .in0(magma_Bits_2_eq_inst6_in0),
    .in1(magma_Bits_2_eq_inst6_in1),
    .out(magma_Bits_2_eq_inst6_out)
);
assign magma_Bits_2_eq_inst7_in0 = mode;
assign magma_Bits_2_eq_inst7_in1 = const_0_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst7 (
    .in0(magma_Bits_2_eq_inst7_in0),
    .in1(magma_Bits_2_eq_inst7_in1),
    .out(magma_Bits_2_eq_inst7_out)
);
assign magma_Bits_2_eq_inst8_in0 = mode;
assign magma_Bits_2_eq_inst8_in1 = const_1_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst8 (
    .in0(magma_Bits_2_eq_inst8_in0),
    .in1(magma_Bits_2_eq_inst8_in1),
    .out(magma_Bits_2_eq_inst8_out)
);
assign magma_Bits_2_eq_inst9_in0 = mode;
assign magma_Bits_2_eq_inst9_in1 = const_0_2_out;
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst9 (
    .in0(magma_Bits_2_eq_inst9_in0),
    .in1(magma_Bits_2_eq_inst9_in1),
    .out(magma_Bits_2_eq_inst9_out)
);
assign O0 = Mux2xOutBits4_inst12_O;
assign O1 = Mux2xOutBit_inst5_O;
assign O2 = Mux2xOutBits4_inst13_O;
assign O3 = Mux2xOutBits4_inst14_O;
endmodule

module RegisterMode (
    input [1:0] mode,
    input [3:0] const_,
    input [3:0] value,
    input clk_en,
    input config_we,
    input [3:0] config_data,
    input CLK,
    output [3:0] O0,
    output [3:0] O1
);
wire [1:0] RegisterMode_comb_inst0_mode;
wire [3:0] RegisterMode_comb_inst0_const_;
wire [3:0] RegisterMode_comb_inst0_value;
wire RegisterMode_comb_inst0_clk_en;
wire RegisterMode_comb_inst0_config_we;
wire [3:0] RegisterMode_comb_inst0_config_data;
wire [3:0] RegisterMode_comb_inst0_self_register_O;
wire [3:0] RegisterMode_comb_inst0_O0;
wire RegisterMode_comb_inst0_O1;
wire [3:0] RegisterMode_comb_inst0_O2;
wire [3:0] RegisterMode_comb_inst0_O3;
wire [3:0] Register_inst0_value;
wire Register_inst0_en;
wire Register_inst0_CLK;
wire [3:0] Register_inst0_O;
assign RegisterMode_comb_inst0_mode = mode;
assign RegisterMode_comb_inst0_const_ = const_;
assign RegisterMode_comb_inst0_value = value;
assign RegisterMode_comb_inst0_clk_en = clk_en;
assign RegisterMode_comb_inst0_config_we = config_we;
assign RegisterMode_comb_inst0_config_data = config_data;
assign RegisterMode_comb_inst0_self_register_O = Register_inst0_O;
RegisterMode_comb RegisterMode_comb_inst0 (
    .mode(RegisterMode_comb_inst0_mode),
    .const_(RegisterMode_comb_inst0_const_),
    .value(RegisterMode_comb_inst0_value),
    .clk_en(RegisterMode_comb_inst0_clk_en),
    .config_we(RegisterMode_comb_inst0_config_we),
    .config_data(RegisterMode_comb_inst0_config_data),
    .self_register_O(RegisterMode_comb_inst0_self_register_O),
    .O0(RegisterMode_comb_inst0_O0),
    .O1(RegisterMode_comb_inst0_O1),
    .O2(RegisterMode_comb_inst0_O2),
    .O3(RegisterMode_comb_inst0_O3)
);
assign Register_inst0_value = RegisterMode_comb_inst0_O0;
assign Register_inst0_en = RegisterMode_comb_inst0_O1;
assign Register_inst0_CLK = CLK;
Register Register_inst0 (
    .value(Register_inst0_value),
    .en(Register_inst0_en),
    .CLK(Register_inst0_CLK),
    .O(Register_inst0_O)
);
assign O0 = RegisterMode_comb_inst0_O2;
assign O1 = RegisterMode_comb_inst0_O3;
endmodule

