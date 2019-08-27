module coreir_reg #(parameter width = 1, parameter clk_posedge = 1, parameter init = 1) (input clk, input [width-1:0] in, output [width-1:0] out);
  reg [width-1:0] outReg=init;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk) begin
    outReg <= in;
  end
  assign out = outReg;
endmodule

module coreir_mux #(parameter width = 1) (input [width-1:0] in0, input [width-1:0] in1, input sel, output [width-1:0] out);
  assign out = sel ? in1 : in0;
endmodule

module coreir_eq #(parameter width = 1) (input [width-1:0] in0, input [width-1:0] in1, output out);
  assign out = in0 == in1;
endmodule

module coreir_const #(parameter width = 1, parameter value = 1) (output [width-1:0] out);
  assign out = value;
endmodule

module coreir_and #(parameter width = 1) (input [width-1:0] in0, input [width-1:0] in1, output [width-1:0] out);
  assign out = in0 & in1;
endmodule

module coreir_add #(parameter width = 1) (input [width-1:0] in0, input [width-1:0] in1, output [width-1:0] out);
  assign out = in0 + in1;
endmodule

module corebit_xor (input in0, input in1, output out);
  assign out = in0 ^ in1;
endmodule

module corebit_not (input in, output out);
  assign out = ~in;
endmodule

module corebit_eq (input I0, input I1, output O);
wire not_inst0_out;
wire xor_inst0_out;
corebit_not not_inst0(.in(xor_inst0_out), .out(not_inst0_out));
corebit_xor xor_inst0(.in0(I0), .in1(I1), .out(xor_inst0_out));
assign O = not_inst0_out;
endmodule

module corebit_const #(parameter value = 1) (output out);
  assign out = value;
endmodule

module corebit_and (input in0, input in1, output out);
  assign out = in0 & in1;
endmodule

module commonlib_muxn__N2__width32 (input [31:0] in_data_0, input [31:0] in_data_1, input [0:0] in_sel, output [31:0] out);
wire [31:0] _join_out;
coreir_mux #(.width(32)) _join(.in0(in_data_0), .in1(in_data_1), .out(_join_out), .sel(in_sel[0]));
assign out = _join_out;
endmodule

module commonlib_muxn__N2__width3 (input [2:0] in_data_0, input [2:0] in_data_1, input [0:0] in_sel, output [2:0] out);
wire [2:0] _join_out;
coreir_mux #(.width(3)) _join(.in0(in_data_0), .in1(in_data_1), .out(_join_out), .sel(in_sel[0]));
assign out = _join_out;
endmodule

module commonlib_muxn__N2__width1 (input [0:0] in_data_0, input [0:0] in_data_1, input [0:0] in_sel, output [0:0] out);
wire [0:0] _join_out;
coreir_mux #(.width(1)) _join(.in0(in_data_0), .in1(in_data_1), .out(_join_out), .sel(in_sel[0]));
assign out = _join_out;
endmodule

module lutN #(parameter N = 1, parameter init = 1) (input [N-1:0] in, output out);
  assign out = init[in];
endmodule

module NENone (input I0, input I1, output O);
wire corebit_eq_inst0_O;
wire not_inst0_out;
corebit_eq corebit_eq_inst0(.I0(I0), .I1(I1), .O(corebit_eq_inst0_O));
corebit_not not_inst0(.in(corebit_eq_inst0_O), .out(not_inst0_out));
assign O = not_inst0_out;
endmodule

module Mux2xOutBits3 (input [2:0] I0, input [2:0] I1, output [2:0] O, input S);
wire [2:0] coreir_commonlib_mux2x3_inst0_out;
commonlib_muxn__N2__width3 coreir_commonlib_mux2x3_inst0(.in_data_0(I0), .in_data_1(I1), .in_sel(S), .out(coreir_commonlib_mux2x3_inst0_out));
assign O = coreir_commonlib_mux2x3_inst0_out;
endmodule

module Mux2xNone (input I0, input I1, output O, input S);
wire [0:0] coreir_commonlib_mux2x1_inst0_out;
commonlib_muxn__N2__width1 coreir_commonlib_mux2x1_inst0(.in_data_0(I0), .in_data_1(I1), .in_sel(S), .out(coreir_commonlib_mux2x1_inst0_out));
assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module Mux2x32 (input [31:0] I0, input [31:0] I1, output [31:0] O, input S);
wire [31:0] coreir_commonlib_mux2x32_inst0_out;
commonlib_muxn__N2__width32 coreir_commonlib_mux2x32_inst0(.in_data_0(I0), .in_data_1(I1), .in_sel(S), .out(coreir_commonlib_mux2x32_inst0_out));
assign O = coreir_commonlib_mux2x32_inst0_out;
endmodule

module LUT2_8 (input I0, input I1, output O);
wire coreir_lut2_inst0_out;
lutN #(.init(4'h8), .N(2)) coreir_lut2_inst0(.in({I1,I0}), .out(coreir_lut2_inst0_out));
assign O = coreir_lut2_inst0_out;
endmodule

module LUT2_4 (input I0, input I1, output O);
wire coreir_lut2_inst0_out;
lutN #(.init(4'h4), .N(2)) coreir_lut2_inst0(.in({I1,I0}), .out(coreir_lut2_inst0_out));
assign O = coreir_lut2_inst0_out;
endmodule

module LUT2_2 (input I0, input I1, output O);
wire coreir_lut2_inst0_out;
lutN #(.init(4'h2), .N(2)) coreir_lut2_inst0(.in({I1,I0}), .out(coreir_lut2_inst0_out));
assign O = coreir_lut2_inst0_out;
endmodule

module LUT2_1 (input I0, input I1, output O);
wire coreir_lut2_inst0_out;
lutN #(.init(4'h1), .N(2)) coreir_lut2_inst0(.in({I1,I0}), .out(coreir_lut2_inst0_out));
assign O = coreir_lut2_inst0_out;
endmodule

module Decoder2 (input [1:0] I, output [3:0] O);
wire LUT2_1_inst0_O;
wire LUT2_2_inst0_O;
wire LUT2_4_inst0_O;
wire LUT2_8_inst0_O;
LUT2_1 LUT2_1_inst0(.I0(I[0]), .I1(I[1]), .O(LUT2_1_inst0_O));
LUT2_2 LUT2_2_inst0(.I0(I[0]), .I1(I[1]), .O(LUT2_2_inst0_O));
LUT2_4 LUT2_4_inst0(.I0(I[0]), .I1(I[1]), .O(LUT2_4_inst0_O));
LUT2_8 LUT2_8_inst0(.I0(I[0]), .I1(I[1]), .O(LUT2_8_inst0_O));
assign O = {LUT2_8_inst0_O,LUT2_4_inst0_O,LUT2_2_inst0_O,LUT2_1_inst0_O};
endmodule

module DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse (input CE, input CLK, input I, output O);
wire Mux2xNone_inst0_O;
wire [0:0] reg_P_inst0_out;
Mux2xNone Mux2xNone_inst0(.I0(reg_P_inst0_out[0]), .I1(I), .O(Mux2xNone_inst0_O), .S(CE));
coreir_reg #(.clk_posedge(1), .init(1'h0), .width(1)) reg_P_inst0(.clk(CLK), .in(Mux2xNone_inst0_O), .out(reg_P_inst0_out));
assign O = reg_P_inst0_out[0];
endmodule

module Register32CE (input CE, input CLK, input [31:0] I, output [31:0] O);
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst0_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst1_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst10_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst11_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst12_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst13_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst14_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst15_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst16_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst17_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst18_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst19_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst2_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst20_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst21_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst22_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst23_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst24_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst25_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst26_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst27_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst28_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst29_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst3_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst30_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst31_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst4_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst5_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst6_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst7_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst8_O;
wire DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst9_O;
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst0(.CE(CE), .CLK(CLK), .I(I[0]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst0_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst1(.CE(CE), .CLK(CLK), .I(I[1]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst1_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst10(.CE(CE), .CLK(CLK), .I(I[10]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst10_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst11(.CE(CE), .CLK(CLK), .I(I[11]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst11_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst12(.CE(CE), .CLK(CLK), .I(I[12]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst12_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst13(.CE(CE), .CLK(CLK), .I(I[13]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst13_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst14(.CE(CE), .CLK(CLK), .I(I[14]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst14_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst15(.CE(CE), .CLK(CLK), .I(I[15]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst15_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst16(.CE(CE), .CLK(CLK), .I(I[16]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst16_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst17(.CE(CE), .CLK(CLK), .I(I[17]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst17_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst18(.CE(CE), .CLK(CLK), .I(I[18]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst18_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst19(.CE(CE), .CLK(CLK), .I(I[19]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst19_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst2(.CE(CE), .CLK(CLK), .I(I[2]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst2_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst20(.CE(CE), .CLK(CLK), .I(I[20]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst20_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst21(.CE(CE), .CLK(CLK), .I(I[21]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst21_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst22(.CE(CE), .CLK(CLK), .I(I[22]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst22_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst23(.CE(CE), .CLK(CLK), .I(I[23]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst23_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst24(.CE(CE), .CLK(CLK), .I(I[24]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst24_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst25(.CE(CE), .CLK(CLK), .I(I[25]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst25_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst26(.CE(CE), .CLK(CLK), .I(I[26]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst26_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst27(.CE(CE), .CLK(CLK), .I(I[27]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst27_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst28(.CE(CE), .CLK(CLK), .I(I[28]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst28_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst29(.CE(CE), .CLK(CLK), .I(I[29]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst29_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst3(.CE(CE), .CLK(CLK), .I(I[3]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst3_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst30(.CE(CE), .CLK(CLK), .I(I[30]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst30_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst31(.CE(CE), .CLK(CLK), .I(I[31]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst31_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst4(.CE(CE), .CLK(CLK), .I(I[4]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst4_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst5(.CE(CE), .CLK(CLK), .I(I[5]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst5_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst6(.CE(CE), .CLK(CLK), .I(I[6]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst6_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst7(.CE(CE), .CLK(CLK), .I(I[7]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst7_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst8(.CE(CE), .CLK(CLK), .I(I[8]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst8_O));
DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst9(.CE(CE), .CLK(CLK), .I(I[9]), .O(DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst9_O));
assign O = {DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst31_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst30_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst29_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst28_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst27_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst26_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst25_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst24_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst23_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst22_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst21_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst20_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst19_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst18_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst17_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst16_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst15_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst14_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst13_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst12_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst11_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst10_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst9_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst8_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst7_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst6_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst5_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst4_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst3_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst2_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst1_O,DFF_init0_has_ceTrue_has_resetFalse_has_async_resetFalse_inst0_O};
endmodule

module RAM4x32 (input CLK, input [1:0] RADDR, output [31:0] RDATA, input [1:0] WADDR, input [31:0] WDATA, input WE);
wire [3:0] Decoder2_inst0_O;
wire [31:0] Mux2x32_inst0_O;
wire [31:0] Mux2x32_inst1_O;
wire [31:0] Mux2x32_inst2_O;
wire [31:0] Register32CE_inst0_O;
wire [31:0] Register32CE_inst1_O;
wire [31:0] Register32CE_inst2_O;
wire [31:0] Register32CE_inst3_O;
wire [3:0] and4_inst0_out;
Decoder2 Decoder2_inst0(.I(WADDR), .O(Decoder2_inst0_O));
Mux2x32 Mux2x32_inst0(.I0(Register32CE_inst0_O), .I1(Register32CE_inst1_O), .O(Mux2x32_inst0_O), .S(RADDR[0]));
Mux2x32 Mux2x32_inst1(.I0(Register32CE_inst2_O), .I1(Register32CE_inst3_O), .O(Mux2x32_inst1_O), .S(RADDR[0]));
Mux2x32 Mux2x32_inst2(.I0(Mux2x32_inst0_O), .I1(Mux2x32_inst1_O), .O(Mux2x32_inst2_O), .S(RADDR[1]));
Register32CE Register32CE_inst0(.CE(and4_inst0_out[0]), .CLK(CLK), .I(WDATA), .O(Register32CE_inst0_O));
Register32CE Register32CE_inst1(.CE(and4_inst0_out[1]), .CLK(CLK), .I(WDATA), .O(Register32CE_inst1_O));
Register32CE Register32CE_inst2(.CE(and4_inst0_out[2]), .CLK(CLK), .I(WDATA), .O(Register32CE_inst2_O));
Register32CE Register32CE_inst3(.CE(and4_inst0_out[3]), .CLK(CLK), .I(WDATA), .O(Register32CE_inst3_O));
coreir_and #(.width(4)) and4_inst0(.in0(Decoder2_inst0_O), .in1({WE,WE,WE,WE}), .out(and4_inst0_out));
assign RDATA = Mux2x32_inst2_O;
endmodule

module FIFO (input CLK, input [7:0] data_in_data_exponent, input data_in_data_sign, input [22:0] data_in_data_significand, output data_in_ready, input data_in_valid, output [7:0] data_out_data_exponent, output data_out_data_sign, output [22:0] data_out_data_significand, input data_out_ready, output data_out_valid);
wire [2:0] Mux2xOutBits3_inst0_O;
wire [2:0] Mux2xOutBits3_inst1_O;
wire NENone_inst0_O;
wire [31:0] RAM4x32_inst0_RDATA;
wire and_inst0_out;
wire and_inst1_out;
wire and_inst2_out;
wire bit_const_1_None_out;
wire [2:0] const_1_3_out;
wire [2:0] coreir_add3_inst0_out;
wire [2:0] coreir_add3_inst1_out;
wire coreir_eq_2_inst0_out;
wire not_inst0_out;
wire not_inst1_out;
wire [2:0] reg_P_inst0_out;
wire [2:0] reg_P_inst1_out;
Mux2xOutBits3 Mux2xOutBits3_inst0(.I0(reg_P_inst1_out), .I1(coreir_add3_inst0_out), .O(Mux2xOutBits3_inst0_O), .S(and_inst1_out));
Mux2xOutBits3 Mux2xOutBits3_inst1(.I0(reg_P_inst0_out), .I1(coreir_add3_inst1_out), .O(Mux2xOutBits3_inst1_O), .S(and_inst2_out));
NENone NENone_inst0(.I0(reg_P_inst0_out[2]), .I1(reg_P_inst1_out[2]), .O(NENone_inst0_O));
RAM4x32 RAM4x32_inst0(.CLK(CLK), .RADDR({reg_P_inst0_out[1],reg_P_inst0_out[0]}), .RDATA(RAM4x32_inst0_RDATA), .WADDR({reg_P_inst1_out[1],reg_P_inst1_out[0]}), .WDATA({data_in_data_significand[22],data_in_data_significand[21],data_in_data_significand[20],data_in_data_significand[19],data_in_data_significand[18],data_in_data_significand[17],data_in_data_significand[16],data_in_data_significand[15],data_in_data_significand[14],data_in_data_significand[13],data_in_data_significand[12],data_in_data_significand[11],data_in_data_significand[10],data_in_data_significand[9],data_in_data_significand[8],data_in_data_significand[7],data_in_data_significand[6],data_in_data_significand[5],data_in_data_significand[4],data_in_data_significand[3],data_in_data_significand[2],data_in_data_significand[1],data_in_data_significand[0],data_in_data_exponent[7],data_in_data_exponent[6],data_in_data_exponent[5],data_in_data_exponent[4],data_in_data_exponent[3],data_in_data_exponent[2],data_in_data_exponent[1],data_in_data_exponent[0],data_in_data_sign}), .WE(and_inst1_out));
corebit_and and_inst0(.in0(coreir_eq_2_inst0_out), .in1(NENone_inst0_O), .out(and_inst0_out));
corebit_and and_inst1(.in0(data_in_valid), .in1(not_inst0_out), .out(and_inst1_out));
corebit_and and_inst2(.in0(data_out_ready), .in1(bit_const_1_None_out), .out(and_inst2_out));
corebit_const #(.value(1)) bit_const_1_None(.out(bit_const_1_None_out));
coreir_const #(.value(3'h1), .width(3)) const_1_3(.out(const_1_3_out));
coreir_add #(.width(3)) coreir_add3_inst0(.in0(reg_P_inst1_out), .in1(const_1_3_out), .out(coreir_add3_inst0_out));
coreir_add #(.width(3)) coreir_add3_inst1(.in0(reg_P_inst0_out), .in1(const_1_3_out), .out(coreir_add3_inst1_out));
coreir_eq #(.width(2)) coreir_eq_2_inst0(.in0({reg_P_inst0_out[1],reg_P_inst0_out[0]}), .in1({reg_P_inst1_out[1],reg_P_inst1_out[0]}), .out(coreir_eq_2_inst0_out));
corebit_not not_inst0(.in(and_inst0_out), .out(not_inst0_out));
corebit_not not_inst1(.in(and_inst0_out), .out(not_inst1_out));
coreir_reg #(.clk_posedge(1), .init(3'h0), .width(3)) reg_P_inst0(.clk(CLK), .in(Mux2xOutBits3_inst1_O), .out(reg_P_inst0_out));
coreir_reg #(.clk_posedge(1), .init(3'h0), .width(3)) reg_P_inst1(.clk(CLK), .in(Mux2xOutBits3_inst0_O), .out(reg_P_inst1_out));
assign data_in_ready = not_inst1_out;
assign data_out_data_exponent = {RAM4x32_inst0_RDATA[8],RAM4x32_inst0_RDATA[7],RAM4x32_inst0_RDATA[6],RAM4x32_inst0_RDATA[5],RAM4x32_inst0_RDATA[4],RAM4x32_inst0_RDATA[3],RAM4x32_inst0_RDATA[2],RAM4x32_inst0_RDATA[1]};
assign data_out_data_sign = RAM4x32_inst0_RDATA[0];
assign data_out_data_significand = {RAM4x32_inst0_RDATA[31],RAM4x32_inst0_RDATA[30],RAM4x32_inst0_RDATA[29],RAM4x32_inst0_RDATA[28],RAM4x32_inst0_RDATA[27],RAM4x32_inst0_RDATA[26],RAM4x32_inst0_RDATA[25],RAM4x32_inst0_RDATA[24],RAM4x32_inst0_RDATA[23],RAM4x32_inst0_RDATA[22],RAM4x32_inst0_RDATA[21],RAM4x32_inst0_RDATA[20],RAM4x32_inst0_RDATA[19],RAM4x32_inst0_RDATA[18],RAM4x32_inst0_RDATA[17],RAM4x32_inst0_RDATA[16],RAM4x32_inst0_RDATA[15],RAM4x32_inst0_RDATA[14],RAM4x32_inst0_RDATA[13],RAM4x32_inst0_RDATA[12],RAM4x32_inst0_RDATA[11],RAM4x32_inst0_RDATA[10],RAM4x32_inst0_RDATA[9]};
assign data_out_valid = and_inst2_out;
endmodule

