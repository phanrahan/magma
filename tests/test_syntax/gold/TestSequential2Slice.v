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

module Register (
    input [63:0] I,
    output [63:0] O,
    input CLK
);
wire reg_P_inst0_clk;
wire [63:0] reg_P_inst0_in;
assign reg_P_inst0_clk = CLK;
assign reg_P_inst0_in = I;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(64'h0000000000000000),
    .width(64)
) reg_P_inst0 (
    .clk(reg_P_inst0_clk),
    .in(reg_P_inst0_in),
    .out(O)
);
endmodule

module Mux56xOutBits8 (
    input [7:0] I0,
    input [7:0] I1,
    input [7:0] I2,
    input [7:0] I3,
    input [7:0] I4,
    input [7:0] I5,
    input [7:0] I6,
    input [7:0] I7,
    input [7:0] I8,
    input [7:0] I9,
    input [7:0] I10,
    input [7:0] I11,
    input [7:0] I12,
    input [7:0] I13,
    input [7:0] I14,
    input [7:0] I15,
    input [7:0] I16,
    input [7:0] I17,
    input [7:0] I18,
    input [7:0] I19,
    input [7:0] I20,
    input [7:0] I21,
    input [7:0] I22,
    input [7:0] I23,
    input [7:0] I24,
    input [7:0] I25,
    input [7:0] I26,
    input [7:0] I27,
    input [7:0] I28,
    input [7:0] I29,
    input [7:0] I30,
    input [7:0] I31,
    input [7:0] I32,
    input [7:0] I33,
    input [7:0] I34,
    input [7:0] I35,
    input [7:0] I36,
    input [7:0] I37,
    input [7:0] I38,
    input [7:0] I39,
    input [7:0] I40,
    input [7:0] I41,
    input [7:0] I42,
    input [7:0] I43,
    input [7:0] I44,
    input [7:0] I45,
    input [7:0] I46,
    input [7:0] I47,
    input [7:0] I48,
    input [7:0] I49,
    input [7:0] I50,
    input [7:0] I51,
    input [7:0] I52,
    input [7:0] I53,
    input [7:0] I54,
    input [7:0] I55,
    input [5:0] S,
    output [7:0] O
);
reg [7:0] coreir_commonlib_mux56x8_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux56x8_inst0_out = I0;
end else if (S == 1) begin
    coreir_commonlib_mux56x8_inst0_out = I1;
end else if (S == 2) begin
    coreir_commonlib_mux56x8_inst0_out = I2;
end else if (S == 3) begin
    coreir_commonlib_mux56x8_inst0_out = I3;
end else if (S == 4) begin
    coreir_commonlib_mux56x8_inst0_out = I4;
end else if (S == 5) begin
    coreir_commonlib_mux56x8_inst0_out = I5;
end else if (S == 6) begin
    coreir_commonlib_mux56x8_inst0_out = I6;
end else if (S == 7) begin
    coreir_commonlib_mux56x8_inst0_out = I7;
end else if (S == 8) begin
    coreir_commonlib_mux56x8_inst0_out = I8;
end else if (S == 9) begin
    coreir_commonlib_mux56x8_inst0_out = I9;
end else if (S == 10) begin
    coreir_commonlib_mux56x8_inst0_out = I10;
end else if (S == 11) begin
    coreir_commonlib_mux56x8_inst0_out = I11;
end else if (S == 12) begin
    coreir_commonlib_mux56x8_inst0_out = I12;
end else if (S == 13) begin
    coreir_commonlib_mux56x8_inst0_out = I13;
end else if (S == 14) begin
    coreir_commonlib_mux56x8_inst0_out = I14;
end else if (S == 15) begin
    coreir_commonlib_mux56x8_inst0_out = I15;
end else if (S == 16) begin
    coreir_commonlib_mux56x8_inst0_out = I16;
end else if (S == 17) begin
    coreir_commonlib_mux56x8_inst0_out = I17;
end else if (S == 18) begin
    coreir_commonlib_mux56x8_inst0_out = I18;
end else if (S == 19) begin
    coreir_commonlib_mux56x8_inst0_out = I19;
end else if (S == 20) begin
    coreir_commonlib_mux56x8_inst0_out = I20;
end else if (S == 21) begin
    coreir_commonlib_mux56x8_inst0_out = I21;
end else if (S == 22) begin
    coreir_commonlib_mux56x8_inst0_out = I22;
end else if (S == 23) begin
    coreir_commonlib_mux56x8_inst0_out = I23;
end else if (S == 24) begin
    coreir_commonlib_mux56x8_inst0_out = I24;
end else if (S == 25) begin
    coreir_commonlib_mux56x8_inst0_out = I25;
end else if (S == 26) begin
    coreir_commonlib_mux56x8_inst0_out = I26;
end else if (S == 27) begin
    coreir_commonlib_mux56x8_inst0_out = I27;
end else if (S == 28) begin
    coreir_commonlib_mux56x8_inst0_out = I28;
end else if (S == 29) begin
    coreir_commonlib_mux56x8_inst0_out = I29;
end else if (S == 30) begin
    coreir_commonlib_mux56x8_inst0_out = I30;
end else if (S == 31) begin
    coreir_commonlib_mux56x8_inst0_out = I31;
end else if (S == 32) begin
    coreir_commonlib_mux56x8_inst0_out = I32;
end else if (S == 33) begin
    coreir_commonlib_mux56x8_inst0_out = I33;
end else if (S == 34) begin
    coreir_commonlib_mux56x8_inst0_out = I34;
end else if (S == 35) begin
    coreir_commonlib_mux56x8_inst0_out = I35;
end else if (S == 36) begin
    coreir_commonlib_mux56x8_inst0_out = I36;
end else if (S == 37) begin
    coreir_commonlib_mux56x8_inst0_out = I37;
end else if (S == 38) begin
    coreir_commonlib_mux56x8_inst0_out = I38;
end else if (S == 39) begin
    coreir_commonlib_mux56x8_inst0_out = I39;
end else if (S == 40) begin
    coreir_commonlib_mux56x8_inst0_out = I40;
end else if (S == 41) begin
    coreir_commonlib_mux56x8_inst0_out = I41;
end else if (S == 42) begin
    coreir_commonlib_mux56x8_inst0_out = I42;
end else if (S == 43) begin
    coreir_commonlib_mux56x8_inst0_out = I43;
end else if (S == 44) begin
    coreir_commonlib_mux56x8_inst0_out = I44;
end else if (S == 45) begin
    coreir_commonlib_mux56x8_inst0_out = I45;
end else if (S == 46) begin
    coreir_commonlib_mux56x8_inst0_out = I46;
end else if (S == 47) begin
    coreir_commonlib_mux56x8_inst0_out = I47;
end else if (S == 48) begin
    coreir_commonlib_mux56x8_inst0_out = I48;
end else if (S == 49) begin
    coreir_commonlib_mux56x8_inst0_out = I49;
end else if (S == 50) begin
    coreir_commonlib_mux56x8_inst0_out = I50;
end else if (S == 51) begin
    coreir_commonlib_mux56x8_inst0_out = I51;
end else if (S == 52) begin
    coreir_commonlib_mux56x8_inst0_out = I52;
end else if (S == 53) begin
    coreir_commonlib_mux56x8_inst0_out = I53;
end else if (S == 54) begin
    coreir_commonlib_mux56x8_inst0_out = I54;
end else begin
    coreir_commonlib_mux56x8_inst0_out = I55;
end
end

assign O = coreir_commonlib_mux56x8_inst0_out;
endmodule

module Mux2xOutBit (
    input I0,
    input I1,
    input S,
    output O
);
reg [0:0] coreir_commonlib_mux2x1_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x1_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x1_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module TestSequential2Slice (
    input [2:0] write_addr,
    input [7:0] write_data,
    input [2:0] read_addr,
    output [7:0] O,
    input CLK
);
wire Mux2xOutBit_inst0_I0;
wire Mux2xOutBit_inst0_I1;
wire Mux2xOutBit_inst0_S;
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_I0;
wire Mux2xOutBit_inst1_I1;
wire Mux2xOutBit_inst1_S;
wire Mux2xOutBit_inst1_O;
wire Mux2xOutBit_inst10_I0;
wire Mux2xOutBit_inst10_I1;
wire Mux2xOutBit_inst10_S;
wire Mux2xOutBit_inst10_O;
wire Mux2xOutBit_inst11_I0;
wire Mux2xOutBit_inst11_I1;
wire Mux2xOutBit_inst11_S;
wire Mux2xOutBit_inst11_O;
wire Mux2xOutBit_inst12_I0;
wire Mux2xOutBit_inst12_I1;
wire Mux2xOutBit_inst12_S;
wire Mux2xOutBit_inst12_O;
wire Mux2xOutBit_inst13_I0;
wire Mux2xOutBit_inst13_I1;
wire Mux2xOutBit_inst13_S;
wire Mux2xOutBit_inst13_O;
wire Mux2xOutBit_inst14_I0;
wire Mux2xOutBit_inst14_I1;
wire Mux2xOutBit_inst14_S;
wire Mux2xOutBit_inst14_O;
wire Mux2xOutBit_inst15_I0;
wire Mux2xOutBit_inst15_I1;
wire Mux2xOutBit_inst15_S;
wire Mux2xOutBit_inst15_O;
wire Mux2xOutBit_inst16_I0;
wire Mux2xOutBit_inst16_I1;
wire Mux2xOutBit_inst16_S;
wire Mux2xOutBit_inst16_O;
wire Mux2xOutBit_inst17_I0;
wire Mux2xOutBit_inst17_I1;
wire Mux2xOutBit_inst17_S;
wire Mux2xOutBit_inst17_O;
wire Mux2xOutBit_inst18_I0;
wire Mux2xOutBit_inst18_I1;
wire Mux2xOutBit_inst18_S;
wire Mux2xOutBit_inst18_O;
wire Mux2xOutBit_inst19_I0;
wire Mux2xOutBit_inst19_I1;
wire Mux2xOutBit_inst19_S;
wire Mux2xOutBit_inst19_O;
wire Mux2xOutBit_inst2_I0;
wire Mux2xOutBit_inst2_I1;
wire Mux2xOutBit_inst2_S;
wire Mux2xOutBit_inst2_O;
wire Mux2xOutBit_inst20_I0;
wire Mux2xOutBit_inst20_I1;
wire Mux2xOutBit_inst20_S;
wire Mux2xOutBit_inst20_O;
wire Mux2xOutBit_inst21_I0;
wire Mux2xOutBit_inst21_I1;
wire Mux2xOutBit_inst21_S;
wire Mux2xOutBit_inst21_O;
wire Mux2xOutBit_inst22_I0;
wire Mux2xOutBit_inst22_I1;
wire Mux2xOutBit_inst22_S;
wire Mux2xOutBit_inst22_O;
wire Mux2xOutBit_inst23_I0;
wire Mux2xOutBit_inst23_I1;
wire Mux2xOutBit_inst23_S;
wire Mux2xOutBit_inst23_O;
wire Mux2xOutBit_inst24_I0;
wire Mux2xOutBit_inst24_I1;
wire Mux2xOutBit_inst24_S;
wire Mux2xOutBit_inst24_O;
wire Mux2xOutBit_inst25_I0;
wire Mux2xOutBit_inst25_I1;
wire Mux2xOutBit_inst25_S;
wire Mux2xOutBit_inst25_O;
wire Mux2xOutBit_inst26_I0;
wire Mux2xOutBit_inst26_I1;
wire Mux2xOutBit_inst26_S;
wire Mux2xOutBit_inst26_O;
wire Mux2xOutBit_inst27_I0;
wire Mux2xOutBit_inst27_I1;
wire Mux2xOutBit_inst27_S;
wire Mux2xOutBit_inst27_O;
wire Mux2xOutBit_inst28_I0;
wire Mux2xOutBit_inst28_I1;
wire Mux2xOutBit_inst28_S;
wire Mux2xOutBit_inst28_O;
wire Mux2xOutBit_inst29_I0;
wire Mux2xOutBit_inst29_I1;
wire Mux2xOutBit_inst29_S;
wire Mux2xOutBit_inst29_O;
wire Mux2xOutBit_inst3_I0;
wire Mux2xOutBit_inst3_I1;
wire Mux2xOutBit_inst3_S;
wire Mux2xOutBit_inst3_O;
wire Mux2xOutBit_inst30_I0;
wire Mux2xOutBit_inst30_I1;
wire Mux2xOutBit_inst30_S;
wire Mux2xOutBit_inst30_O;
wire Mux2xOutBit_inst31_I0;
wire Mux2xOutBit_inst31_I1;
wire Mux2xOutBit_inst31_S;
wire Mux2xOutBit_inst31_O;
wire Mux2xOutBit_inst32_I0;
wire Mux2xOutBit_inst32_I1;
wire Mux2xOutBit_inst32_S;
wire Mux2xOutBit_inst32_O;
wire Mux2xOutBit_inst33_I0;
wire Mux2xOutBit_inst33_I1;
wire Mux2xOutBit_inst33_S;
wire Mux2xOutBit_inst33_O;
wire Mux2xOutBit_inst34_I0;
wire Mux2xOutBit_inst34_I1;
wire Mux2xOutBit_inst34_S;
wire Mux2xOutBit_inst34_O;
wire Mux2xOutBit_inst35_I0;
wire Mux2xOutBit_inst35_I1;
wire Mux2xOutBit_inst35_S;
wire Mux2xOutBit_inst35_O;
wire Mux2xOutBit_inst36_I0;
wire Mux2xOutBit_inst36_I1;
wire Mux2xOutBit_inst36_S;
wire Mux2xOutBit_inst36_O;
wire Mux2xOutBit_inst37_I0;
wire Mux2xOutBit_inst37_I1;
wire Mux2xOutBit_inst37_S;
wire Mux2xOutBit_inst37_O;
wire Mux2xOutBit_inst38_I0;
wire Mux2xOutBit_inst38_I1;
wire Mux2xOutBit_inst38_S;
wire Mux2xOutBit_inst38_O;
wire Mux2xOutBit_inst39_I0;
wire Mux2xOutBit_inst39_I1;
wire Mux2xOutBit_inst39_S;
wire Mux2xOutBit_inst39_O;
wire Mux2xOutBit_inst4_I0;
wire Mux2xOutBit_inst4_I1;
wire Mux2xOutBit_inst4_S;
wire Mux2xOutBit_inst4_O;
wire Mux2xOutBit_inst40_I0;
wire Mux2xOutBit_inst40_I1;
wire Mux2xOutBit_inst40_S;
wire Mux2xOutBit_inst40_O;
wire Mux2xOutBit_inst41_I0;
wire Mux2xOutBit_inst41_I1;
wire Mux2xOutBit_inst41_S;
wire Mux2xOutBit_inst41_O;
wire Mux2xOutBit_inst42_I0;
wire Mux2xOutBit_inst42_I1;
wire Mux2xOutBit_inst42_S;
wire Mux2xOutBit_inst42_O;
wire Mux2xOutBit_inst43_I0;
wire Mux2xOutBit_inst43_I1;
wire Mux2xOutBit_inst43_S;
wire Mux2xOutBit_inst43_O;
wire Mux2xOutBit_inst44_I0;
wire Mux2xOutBit_inst44_I1;
wire Mux2xOutBit_inst44_S;
wire Mux2xOutBit_inst44_O;
wire Mux2xOutBit_inst45_I0;
wire Mux2xOutBit_inst45_I1;
wire Mux2xOutBit_inst45_S;
wire Mux2xOutBit_inst45_O;
wire Mux2xOutBit_inst46_I0;
wire Mux2xOutBit_inst46_I1;
wire Mux2xOutBit_inst46_S;
wire Mux2xOutBit_inst46_O;
wire Mux2xOutBit_inst47_I0;
wire Mux2xOutBit_inst47_I1;
wire Mux2xOutBit_inst47_S;
wire Mux2xOutBit_inst47_O;
wire Mux2xOutBit_inst48_I0;
wire Mux2xOutBit_inst48_I1;
wire Mux2xOutBit_inst48_S;
wire Mux2xOutBit_inst48_O;
wire Mux2xOutBit_inst49_I0;
wire Mux2xOutBit_inst49_I1;
wire Mux2xOutBit_inst49_S;
wire Mux2xOutBit_inst49_O;
wire Mux2xOutBit_inst5_I0;
wire Mux2xOutBit_inst5_I1;
wire Mux2xOutBit_inst5_S;
wire Mux2xOutBit_inst5_O;
wire Mux2xOutBit_inst50_I0;
wire Mux2xOutBit_inst50_I1;
wire Mux2xOutBit_inst50_S;
wire Mux2xOutBit_inst50_O;
wire Mux2xOutBit_inst51_I0;
wire Mux2xOutBit_inst51_I1;
wire Mux2xOutBit_inst51_S;
wire Mux2xOutBit_inst51_O;
wire Mux2xOutBit_inst52_I0;
wire Mux2xOutBit_inst52_I1;
wire Mux2xOutBit_inst52_S;
wire Mux2xOutBit_inst52_O;
wire Mux2xOutBit_inst53_I0;
wire Mux2xOutBit_inst53_I1;
wire Mux2xOutBit_inst53_S;
wire Mux2xOutBit_inst53_O;
wire Mux2xOutBit_inst54_I0;
wire Mux2xOutBit_inst54_I1;
wire Mux2xOutBit_inst54_S;
wire Mux2xOutBit_inst54_O;
wire Mux2xOutBit_inst55_I0;
wire Mux2xOutBit_inst55_I1;
wire Mux2xOutBit_inst55_S;
wire Mux2xOutBit_inst55_O;
wire Mux2xOutBit_inst56_I0;
wire Mux2xOutBit_inst56_I1;
wire Mux2xOutBit_inst56_S;
wire Mux2xOutBit_inst56_O;
wire Mux2xOutBit_inst57_I0;
wire Mux2xOutBit_inst57_I1;
wire Mux2xOutBit_inst57_S;
wire Mux2xOutBit_inst57_O;
wire Mux2xOutBit_inst58_I0;
wire Mux2xOutBit_inst58_I1;
wire Mux2xOutBit_inst58_S;
wire Mux2xOutBit_inst58_O;
wire Mux2xOutBit_inst59_I0;
wire Mux2xOutBit_inst59_I1;
wire Mux2xOutBit_inst59_S;
wire Mux2xOutBit_inst59_O;
wire Mux2xOutBit_inst6_I0;
wire Mux2xOutBit_inst6_I1;
wire Mux2xOutBit_inst6_S;
wire Mux2xOutBit_inst6_O;
wire Mux2xOutBit_inst60_I0;
wire Mux2xOutBit_inst60_I1;
wire Mux2xOutBit_inst60_S;
wire Mux2xOutBit_inst60_O;
wire Mux2xOutBit_inst61_I0;
wire Mux2xOutBit_inst61_I1;
wire Mux2xOutBit_inst61_S;
wire Mux2xOutBit_inst61_O;
wire Mux2xOutBit_inst62_I0;
wire Mux2xOutBit_inst62_I1;
wire Mux2xOutBit_inst62_S;
wire Mux2xOutBit_inst62_O;
wire Mux2xOutBit_inst63_I0;
wire Mux2xOutBit_inst63_I1;
wire Mux2xOutBit_inst63_S;
wire Mux2xOutBit_inst63_O;
wire Mux2xOutBit_inst7_I0;
wire Mux2xOutBit_inst7_I1;
wire Mux2xOutBit_inst7_S;
wire Mux2xOutBit_inst7_O;
wire Mux2xOutBit_inst8_I0;
wire Mux2xOutBit_inst8_I1;
wire Mux2xOutBit_inst8_S;
wire Mux2xOutBit_inst8_O;
wire Mux2xOutBit_inst9_I0;
wire Mux2xOutBit_inst9_I1;
wire Mux2xOutBit_inst9_S;
wire Mux2xOutBit_inst9_O;
wire [7:0] Mux56xOutBits8_inst0_I0;
wire [7:0] Mux56xOutBits8_inst0_I1;
wire [7:0] Mux56xOutBits8_inst0_I2;
wire [7:0] Mux56xOutBits8_inst0_I3;
wire [7:0] Mux56xOutBits8_inst0_I4;
wire [7:0] Mux56xOutBits8_inst0_I5;
wire [7:0] Mux56xOutBits8_inst0_I6;
wire [7:0] Mux56xOutBits8_inst0_I7;
wire [7:0] Mux56xOutBits8_inst0_I8;
wire [7:0] Mux56xOutBits8_inst0_I9;
wire [7:0] Mux56xOutBits8_inst0_I10;
wire [7:0] Mux56xOutBits8_inst0_I11;
wire [7:0] Mux56xOutBits8_inst0_I12;
wire [7:0] Mux56xOutBits8_inst0_I13;
wire [7:0] Mux56xOutBits8_inst0_I14;
wire [7:0] Mux56xOutBits8_inst0_I15;
wire [7:0] Mux56xOutBits8_inst0_I16;
wire [7:0] Mux56xOutBits8_inst0_I17;
wire [7:0] Mux56xOutBits8_inst0_I18;
wire [7:0] Mux56xOutBits8_inst0_I19;
wire [7:0] Mux56xOutBits8_inst0_I20;
wire [7:0] Mux56xOutBits8_inst0_I21;
wire [7:0] Mux56xOutBits8_inst0_I22;
wire [7:0] Mux56xOutBits8_inst0_I23;
wire [7:0] Mux56xOutBits8_inst0_I24;
wire [7:0] Mux56xOutBits8_inst0_I25;
wire [7:0] Mux56xOutBits8_inst0_I26;
wire [7:0] Mux56xOutBits8_inst0_I27;
wire [7:0] Mux56xOutBits8_inst0_I28;
wire [7:0] Mux56xOutBits8_inst0_I29;
wire [7:0] Mux56xOutBits8_inst0_I30;
wire [7:0] Mux56xOutBits8_inst0_I31;
wire [7:0] Mux56xOutBits8_inst0_I32;
wire [7:0] Mux56xOutBits8_inst0_I33;
wire [7:0] Mux56xOutBits8_inst0_I34;
wire [7:0] Mux56xOutBits8_inst0_I35;
wire [7:0] Mux56xOutBits8_inst0_I36;
wire [7:0] Mux56xOutBits8_inst0_I37;
wire [7:0] Mux56xOutBits8_inst0_I38;
wire [7:0] Mux56xOutBits8_inst0_I39;
wire [7:0] Mux56xOutBits8_inst0_I40;
wire [7:0] Mux56xOutBits8_inst0_I41;
wire [7:0] Mux56xOutBits8_inst0_I42;
wire [7:0] Mux56xOutBits8_inst0_I43;
wire [7:0] Mux56xOutBits8_inst0_I44;
wire [7:0] Mux56xOutBits8_inst0_I45;
wire [7:0] Mux56xOutBits8_inst0_I46;
wire [7:0] Mux56xOutBits8_inst0_I47;
wire [7:0] Mux56xOutBits8_inst0_I48;
wire [7:0] Mux56xOutBits8_inst0_I49;
wire [7:0] Mux56xOutBits8_inst0_I50;
wire [7:0] Mux56xOutBits8_inst0_I51;
wire [7:0] Mux56xOutBits8_inst0_I52;
wire [7:0] Mux56xOutBits8_inst0_I53;
wire [7:0] Mux56xOutBits8_inst0_I54;
wire [7:0] Mux56xOutBits8_inst0_I55;
wire [5:0] Mux56xOutBits8_inst0_S;
wire [63:0] Register_inst0_I;
wire [63:0] Register_inst0_O;
wire Register_inst0_CLK;
wire [5:0] magma_Bits_6_mul_inst1_out;
wire [5:0] magma_Bits_6_sub_inst0_out;
wire [5:0] magma_Bits_6_sub_inst10_out;
wire [5:0] magma_Bits_6_sub_inst100_out;
wire [5:0] magma_Bits_6_sub_inst102_out;
wire [5:0] magma_Bits_6_sub_inst104_out;
wire [5:0] magma_Bits_6_sub_inst106_out;
wire [5:0] magma_Bits_6_sub_inst108_out;
wire [5:0] magma_Bits_6_sub_inst110_out;
wire [5:0] magma_Bits_6_sub_inst112_out;
wire [5:0] magma_Bits_6_sub_inst114_out;
wire [5:0] magma_Bits_6_sub_inst116_out;
wire [5:0] magma_Bits_6_sub_inst118_out;
wire [5:0] magma_Bits_6_sub_inst12_out;
wire [5:0] magma_Bits_6_sub_inst120_out;
wire [5:0] magma_Bits_6_sub_inst122_out;
wire [5:0] magma_Bits_6_sub_inst124_out;
wire [5:0] magma_Bits_6_sub_inst126_out;
wire [5:0] magma_Bits_6_sub_inst14_out;
wire [5:0] magma_Bits_6_sub_inst16_out;
wire [5:0] magma_Bits_6_sub_inst18_out;
wire [5:0] magma_Bits_6_sub_inst2_out;
wire [5:0] magma_Bits_6_sub_inst20_out;
wire [5:0] magma_Bits_6_sub_inst22_out;
wire [5:0] magma_Bits_6_sub_inst24_out;
wire [5:0] magma_Bits_6_sub_inst26_out;
wire [5:0] magma_Bits_6_sub_inst28_out;
wire [5:0] magma_Bits_6_sub_inst30_out;
wire [5:0] magma_Bits_6_sub_inst32_out;
wire [5:0] magma_Bits_6_sub_inst34_out;
wire [5:0] magma_Bits_6_sub_inst36_out;
wire [5:0] magma_Bits_6_sub_inst38_out;
wire [5:0] magma_Bits_6_sub_inst4_out;
wire [5:0] magma_Bits_6_sub_inst40_out;
wire [5:0] magma_Bits_6_sub_inst42_out;
wire [5:0] magma_Bits_6_sub_inst44_out;
wire [5:0] magma_Bits_6_sub_inst46_out;
wire [5:0] magma_Bits_6_sub_inst48_out;
wire [5:0] magma_Bits_6_sub_inst50_out;
wire [5:0] magma_Bits_6_sub_inst52_out;
wire [5:0] magma_Bits_6_sub_inst54_out;
wire [5:0] magma_Bits_6_sub_inst56_out;
wire [5:0] magma_Bits_6_sub_inst58_out;
wire [5:0] magma_Bits_6_sub_inst6_out;
wire [5:0] magma_Bits_6_sub_inst60_out;
wire [5:0] magma_Bits_6_sub_inst62_out;
wire [5:0] magma_Bits_6_sub_inst64_out;
wire [5:0] magma_Bits_6_sub_inst66_out;
wire [5:0] magma_Bits_6_sub_inst68_out;
wire [5:0] magma_Bits_6_sub_inst70_out;
wire [5:0] magma_Bits_6_sub_inst72_out;
wire [5:0] magma_Bits_6_sub_inst74_out;
wire [5:0] magma_Bits_6_sub_inst76_out;
wire [5:0] magma_Bits_6_sub_inst78_out;
wire [5:0] magma_Bits_6_sub_inst8_out;
wire [5:0] magma_Bits_6_sub_inst80_out;
wire [5:0] magma_Bits_6_sub_inst82_out;
wire [5:0] magma_Bits_6_sub_inst84_out;
wire [5:0] magma_Bits_6_sub_inst86_out;
wire [5:0] magma_Bits_6_sub_inst88_out;
wire [5:0] magma_Bits_6_sub_inst90_out;
wire [5:0] magma_Bits_6_sub_inst92_out;
wire [5:0] magma_Bits_6_sub_inst94_out;
wire [5:0] magma_Bits_6_sub_inst96_out;
wire [5:0] magma_Bits_6_sub_inst98_out;
wire [7:0] magma_Bits_8_lshr_inst0_out;
wire [7:0] magma_Bits_8_lshr_inst1_out;
wire [7:0] magma_Bits_8_lshr_inst10_out;
wire [7:0] magma_Bits_8_lshr_inst11_out;
wire [7:0] magma_Bits_8_lshr_inst12_out;
wire [7:0] magma_Bits_8_lshr_inst13_out;
wire [7:0] magma_Bits_8_lshr_inst14_out;
wire [7:0] magma_Bits_8_lshr_inst15_out;
wire [7:0] magma_Bits_8_lshr_inst16_out;
wire [7:0] magma_Bits_8_lshr_inst17_out;
wire [7:0] magma_Bits_8_lshr_inst18_out;
wire [7:0] magma_Bits_8_lshr_inst19_out;
wire [7:0] magma_Bits_8_lshr_inst2_out;
wire [7:0] magma_Bits_8_lshr_inst20_out;
wire [7:0] magma_Bits_8_lshr_inst21_out;
wire [7:0] magma_Bits_8_lshr_inst22_out;
wire [7:0] magma_Bits_8_lshr_inst23_out;
wire [7:0] magma_Bits_8_lshr_inst24_out;
wire [7:0] magma_Bits_8_lshr_inst25_out;
wire [7:0] magma_Bits_8_lshr_inst26_out;
wire [7:0] magma_Bits_8_lshr_inst27_out;
wire [7:0] magma_Bits_8_lshr_inst28_out;
wire [7:0] magma_Bits_8_lshr_inst29_out;
wire [7:0] magma_Bits_8_lshr_inst3_out;
wire [7:0] magma_Bits_8_lshr_inst30_out;
wire [7:0] magma_Bits_8_lshr_inst31_out;
wire [7:0] magma_Bits_8_lshr_inst32_out;
wire [7:0] magma_Bits_8_lshr_inst33_out;
wire [7:0] magma_Bits_8_lshr_inst34_out;
wire [7:0] magma_Bits_8_lshr_inst35_out;
wire [7:0] magma_Bits_8_lshr_inst36_out;
wire [7:0] magma_Bits_8_lshr_inst37_out;
wire [7:0] magma_Bits_8_lshr_inst38_out;
wire [7:0] magma_Bits_8_lshr_inst39_out;
wire [7:0] magma_Bits_8_lshr_inst4_out;
wire [7:0] magma_Bits_8_lshr_inst40_out;
wire [7:0] magma_Bits_8_lshr_inst41_out;
wire [7:0] magma_Bits_8_lshr_inst42_out;
wire [7:0] magma_Bits_8_lshr_inst43_out;
wire [7:0] magma_Bits_8_lshr_inst44_out;
wire [7:0] magma_Bits_8_lshr_inst45_out;
wire [7:0] magma_Bits_8_lshr_inst46_out;
wire [7:0] magma_Bits_8_lshr_inst47_out;
wire [7:0] magma_Bits_8_lshr_inst48_out;
wire [7:0] magma_Bits_8_lshr_inst49_out;
wire [7:0] magma_Bits_8_lshr_inst5_out;
wire [7:0] magma_Bits_8_lshr_inst50_out;
wire [7:0] magma_Bits_8_lshr_inst51_out;
wire [7:0] magma_Bits_8_lshr_inst52_out;
wire [7:0] magma_Bits_8_lshr_inst53_out;
wire [7:0] magma_Bits_8_lshr_inst54_out;
wire [7:0] magma_Bits_8_lshr_inst55_out;
wire [7:0] magma_Bits_8_lshr_inst56_out;
wire [7:0] magma_Bits_8_lshr_inst57_out;
wire [7:0] magma_Bits_8_lshr_inst58_out;
wire [7:0] magma_Bits_8_lshr_inst59_out;
wire [7:0] magma_Bits_8_lshr_inst6_out;
wire [7:0] magma_Bits_8_lshr_inst60_out;
wire [7:0] magma_Bits_8_lshr_inst61_out;
wire [7:0] magma_Bits_8_lshr_inst62_out;
wire [7:0] magma_Bits_8_lshr_inst63_out;
wire [7:0] magma_Bits_8_lshr_inst7_out;
wire [7:0] magma_Bits_8_lshr_inst8_out;
wire [7:0] magma_Bits_8_lshr_inst9_out;
assign Mux2xOutBit_inst0_I0 = Register_inst0_O[0];
assign Mux2xOutBit_inst0_I1 = magma_Bits_8_lshr_inst0_out[0];
assign Mux2xOutBit_inst0_S = 1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h00);
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(Mux2xOutBit_inst0_I0),
    .I1(Mux2xOutBit_inst0_I1),
    .S(Mux2xOutBit_inst0_S),
    .O(Mux2xOutBit_inst0_O)
);
assign Mux2xOutBit_inst1_I0 = Register_inst0_O[1];
assign Mux2xOutBit_inst1_I1 = magma_Bits_8_lshr_inst1_out[0];
assign Mux2xOutBit_inst1_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h01)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h01);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(Mux2xOutBit_inst1_I0),
    .I1(Mux2xOutBit_inst1_I1),
    .S(Mux2xOutBit_inst1_S),
    .O(Mux2xOutBit_inst1_O)
);
assign Mux2xOutBit_inst10_I0 = Register_inst0_O[10];
assign Mux2xOutBit_inst10_I1 = magma_Bits_8_lshr_inst10_out[0];
assign Mux2xOutBit_inst10_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h0a)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0a);
Mux2xOutBit Mux2xOutBit_inst10 (
    .I0(Mux2xOutBit_inst10_I0),
    .I1(Mux2xOutBit_inst10_I1),
    .S(Mux2xOutBit_inst10_S),
    .O(Mux2xOutBit_inst10_O)
);
assign Mux2xOutBit_inst11_I0 = Register_inst0_O[11];
assign Mux2xOutBit_inst11_I1 = magma_Bits_8_lshr_inst11_out[0];
assign Mux2xOutBit_inst11_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h0b)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0b);
Mux2xOutBit Mux2xOutBit_inst11 (
    .I0(Mux2xOutBit_inst11_I0),
    .I1(Mux2xOutBit_inst11_I1),
    .S(Mux2xOutBit_inst11_S),
    .O(Mux2xOutBit_inst11_O)
);
assign Mux2xOutBit_inst12_I0 = Register_inst0_O[12];
assign Mux2xOutBit_inst12_I1 = magma_Bits_8_lshr_inst12_out[0];
assign Mux2xOutBit_inst12_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h0c)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0c);
Mux2xOutBit Mux2xOutBit_inst12 (
    .I0(Mux2xOutBit_inst12_I0),
    .I1(Mux2xOutBit_inst12_I1),
    .S(Mux2xOutBit_inst12_S),
    .O(Mux2xOutBit_inst12_O)
);
assign Mux2xOutBit_inst13_I0 = Register_inst0_O[13];
assign Mux2xOutBit_inst13_I1 = magma_Bits_8_lshr_inst13_out[0];
assign Mux2xOutBit_inst13_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h0d)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0d);
Mux2xOutBit Mux2xOutBit_inst13 (
    .I0(Mux2xOutBit_inst13_I0),
    .I1(Mux2xOutBit_inst13_I1),
    .S(Mux2xOutBit_inst13_S),
    .O(Mux2xOutBit_inst13_O)
);
assign Mux2xOutBit_inst14_I0 = Register_inst0_O[14];
assign Mux2xOutBit_inst14_I1 = magma_Bits_8_lshr_inst14_out[0];
assign Mux2xOutBit_inst14_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h0e)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0e);
Mux2xOutBit Mux2xOutBit_inst14 (
    .I0(Mux2xOutBit_inst14_I0),
    .I1(Mux2xOutBit_inst14_I1),
    .S(Mux2xOutBit_inst14_S),
    .O(Mux2xOutBit_inst14_O)
);
assign Mux2xOutBit_inst15_I0 = Register_inst0_O[15];
assign Mux2xOutBit_inst15_I1 = magma_Bits_8_lshr_inst15_out[0];
assign Mux2xOutBit_inst15_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h0f)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0f);
Mux2xOutBit Mux2xOutBit_inst15 (
    .I0(Mux2xOutBit_inst15_I0),
    .I1(Mux2xOutBit_inst15_I1),
    .S(Mux2xOutBit_inst15_S),
    .O(Mux2xOutBit_inst15_O)
);
assign Mux2xOutBit_inst16_I0 = Register_inst0_O[16];
assign Mux2xOutBit_inst16_I1 = magma_Bits_8_lshr_inst16_out[0];
assign Mux2xOutBit_inst16_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h10)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h10);
Mux2xOutBit Mux2xOutBit_inst16 (
    .I0(Mux2xOutBit_inst16_I0),
    .I1(Mux2xOutBit_inst16_I1),
    .S(Mux2xOutBit_inst16_S),
    .O(Mux2xOutBit_inst16_O)
);
assign Mux2xOutBit_inst17_I0 = Register_inst0_O[17];
assign Mux2xOutBit_inst17_I1 = magma_Bits_8_lshr_inst17_out[0];
assign Mux2xOutBit_inst17_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h11)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h11);
Mux2xOutBit Mux2xOutBit_inst17 (
    .I0(Mux2xOutBit_inst17_I0),
    .I1(Mux2xOutBit_inst17_I1),
    .S(Mux2xOutBit_inst17_S),
    .O(Mux2xOutBit_inst17_O)
);
assign Mux2xOutBit_inst18_I0 = Register_inst0_O[18];
assign Mux2xOutBit_inst18_I1 = magma_Bits_8_lshr_inst18_out[0];
assign Mux2xOutBit_inst18_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h12)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h12);
Mux2xOutBit Mux2xOutBit_inst18 (
    .I0(Mux2xOutBit_inst18_I0),
    .I1(Mux2xOutBit_inst18_I1),
    .S(Mux2xOutBit_inst18_S),
    .O(Mux2xOutBit_inst18_O)
);
assign Mux2xOutBit_inst19_I0 = Register_inst0_O[19];
assign Mux2xOutBit_inst19_I1 = magma_Bits_8_lshr_inst19_out[0];
assign Mux2xOutBit_inst19_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h13)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h13);
Mux2xOutBit Mux2xOutBit_inst19 (
    .I0(Mux2xOutBit_inst19_I0),
    .I1(Mux2xOutBit_inst19_I1),
    .S(Mux2xOutBit_inst19_S),
    .O(Mux2xOutBit_inst19_O)
);
assign Mux2xOutBit_inst2_I0 = Register_inst0_O[2];
assign Mux2xOutBit_inst2_I1 = magma_Bits_8_lshr_inst2_out[0];
assign Mux2xOutBit_inst2_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h02)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h02);
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(Mux2xOutBit_inst2_I0),
    .I1(Mux2xOutBit_inst2_I1),
    .S(Mux2xOutBit_inst2_S),
    .O(Mux2xOutBit_inst2_O)
);
assign Mux2xOutBit_inst20_I0 = Register_inst0_O[20];
assign Mux2xOutBit_inst20_I1 = magma_Bits_8_lshr_inst20_out[0];
assign Mux2xOutBit_inst20_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h14)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h14);
Mux2xOutBit Mux2xOutBit_inst20 (
    .I0(Mux2xOutBit_inst20_I0),
    .I1(Mux2xOutBit_inst20_I1),
    .S(Mux2xOutBit_inst20_S),
    .O(Mux2xOutBit_inst20_O)
);
assign Mux2xOutBit_inst21_I0 = Register_inst0_O[21];
assign Mux2xOutBit_inst21_I1 = magma_Bits_8_lshr_inst21_out[0];
assign Mux2xOutBit_inst21_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h15)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h15);
Mux2xOutBit Mux2xOutBit_inst21 (
    .I0(Mux2xOutBit_inst21_I0),
    .I1(Mux2xOutBit_inst21_I1),
    .S(Mux2xOutBit_inst21_S),
    .O(Mux2xOutBit_inst21_O)
);
assign Mux2xOutBit_inst22_I0 = Register_inst0_O[22];
assign Mux2xOutBit_inst22_I1 = magma_Bits_8_lshr_inst22_out[0];
assign Mux2xOutBit_inst22_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h16)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h16);
Mux2xOutBit Mux2xOutBit_inst22 (
    .I0(Mux2xOutBit_inst22_I0),
    .I1(Mux2xOutBit_inst22_I1),
    .S(Mux2xOutBit_inst22_S),
    .O(Mux2xOutBit_inst22_O)
);
assign Mux2xOutBit_inst23_I0 = Register_inst0_O[23];
assign Mux2xOutBit_inst23_I1 = magma_Bits_8_lshr_inst23_out[0];
assign Mux2xOutBit_inst23_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h17)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h17);
Mux2xOutBit Mux2xOutBit_inst23 (
    .I0(Mux2xOutBit_inst23_I0),
    .I1(Mux2xOutBit_inst23_I1),
    .S(Mux2xOutBit_inst23_S),
    .O(Mux2xOutBit_inst23_O)
);
assign Mux2xOutBit_inst24_I0 = Register_inst0_O[24];
assign Mux2xOutBit_inst24_I1 = magma_Bits_8_lshr_inst24_out[0];
assign Mux2xOutBit_inst24_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h18)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h18);
Mux2xOutBit Mux2xOutBit_inst24 (
    .I0(Mux2xOutBit_inst24_I0),
    .I1(Mux2xOutBit_inst24_I1),
    .S(Mux2xOutBit_inst24_S),
    .O(Mux2xOutBit_inst24_O)
);
assign Mux2xOutBit_inst25_I0 = Register_inst0_O[25];
assign Mux2xOutBit_inst25_I1 = magma_Bits_8_lshr_inst25_out[0];
assign Mux2xOutBit_inst25_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h19)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h19);
Mux2xOutBit Mux2xOutBit_inst25 (
    .I0(Mux2xOutBit_inst25_I0),
    .I1(Mux2xOutBit_inst25_I1),
    .S(Mux2xOutBit_inst25_S),
    .O(Mux2xOutBit_inst25_O)
);
assign Mux2xOutBit_inst26_I0 = Register_inst0_O[26];
assign Mux2xOutBit_inst26_I1 = magma_Bits_8_lshr_inst26_out[0];
assign Mux2xOutBit_inst26_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h1a)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1a);
Mux2xOutBit Mux2xOutBit_inst26 (
    .I0(Mux2xOutBit_inst26_I0),
    .I1(Mux2xOutBit_inst26_I1),
    .S(Mux2xOutBit_inst26_S),
    .O(Mux2xOutBit_inst26_O)
);
assign Mux2xOutBit_inst27_I0 = Register_inst0_O[27];
assign Mux2xOutBit_inst27_I1 = magma_Bits_8_lshr_inst27_out[0];
assign Mux2xOutBit_inst27_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h1b)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1b);
Mux2xOutBit Mux2xOutBit_inst27 (
    .I0(Mux2xOutBit_inst27_I0),
    .I1(Mux2xOutBit_inst27_I1),
    .S(Mux2xOutBit_inst27_S),
    .O(Mux2xOutBit_inst27_O)
);
assign Mux2xOutBit_inst28_I0 = Register_inst0_O[28];
assign Mux2xOutBit_inst28_I1 = magma_Bits_8_lshr_inst28_out[0];
assign Mux2xOutBit_inst28_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h1c)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1c);
Mux2xOutBit Mux2xOutBit_inst28 (
    .I0(Mux2xOutBit_inst28_I0),
    .I1(Mux2xOutBit_inst28_I1),
    .S(Mux2xOutBit_inst28_S),
    .O(Mux2xOutBit_inst28_O)
);
assign Mux2xOutBit_inst29_I0 = Register_inst0_O[29];
assign Mux2xOutBit_inst29_I1 = magma_Bits_8_lshr_inst29_out[0];
assign Mux2xOutBit_inst29_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h1d)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1d);
Mux2xOutBit Mux2xOutBit_inst29 (
    .I0(Mux2xOutBit_inst29_I0),
    .I1(Mux2xOutBit_inst29_I1),
    .S(Mux2xOutBit_inst29_S),
    .O(Mux2xOutBit_inst29_O)
);
assign Mux2xOutBit_inst3_I0 = Register_inst0_O[3];
assign Mux2xOutBit_inst3_I1 = magma_Bits_8_lshr_inst3_out[0];
assign Mux2xOutBit_inst3_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h03)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h03);
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(Mux2xOutBit_inst3_I0),
    .I1(Mux2xOutBit_inst3_I1),
    .S(Mux2xOutBit_inst3_S),
    .O(Mux2xOutBit_inst3_O)
);
assign Mux2xOutBit_inst30_I0 = Register_inst0_O[30];
assign Mux2xOutBit_inst30_I1 = magma_Bits_8_lshr_inst30_out[0];
assign Mux2xOutBit_inst30_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h1e)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1e);
Mux2xOutBit Mux2xOutBit_inst30 (
    .I0(Mux2xOutBit_inst30_I0),
    .I1(Mux2xOutBit_inst30_I1),
    .S(Mux2xOutBit_inst30_S),
    .O(Mux2xOutBit_inst30_O)
);
assign Mux2xOutBit_inst31_I0 = Register_inst0_O[31];
assign Mux2xOutBit_inst31_I1 = magma_Bits_8_lshr_inst31_out[0];
assign Mux2xOutBit_inst31_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h1f)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1f);
Mux2xOutBit Mux2xOutBit_inst31 (
    .I0(Mux2xOutBit_inst31_I0),
    .I1(Mux2xOutBit_inst31_I1),
    .S(Mux2xOutBit_inst31_S),
    .O(Mux2xOutBit_inst31_O)
);
assign Mux2xOutBit_inst32_I0 = Register_inst0_O[32];
assign Mux2xOutBit_inst32_I1 = magma_Bits_8_lshr_inst32_out[0];
assign Mux2xOutBit_inst32_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h20)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h20);
Mux2xOutBit Mux2xOutBit_inst32 (
    .I0(Mux2xOutBit_inst32_I0),
    .I1(Mux2xOutBit_inst32_I1),
    .S(Mux2xOutBit_inst32_S),
    .O(Mux2xOutBit_inst32_O)
);
assign Mux2xOutBit_inst33_I0 = Register_inst0_O[33];
assign Mux2xOutBit_inst33_I1 = magma_Bits_8_lshr_inst33_out[0];
assign Mux2xOutBit_inst33_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h21)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h21);
Mux2xOutBit Mux2xOutBit_inst33 (
    .I0(Mux2xOutBit_inst33_I0),
    .I1(Mux2xOutBit_inst33_I1),
    .S(Mux2xOutBit_inst33_S),
    .O(Mux2xOutBit_inst33_O)
);
assign Mux2xOutBit_inst34_I0 = Register_inst0_O[34];
assign Mux2xOutBit_inst34_I1 = magma_Bits_8_lshr_inst34_out[0];
assign Mux2xOutBit_inst34_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h22)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h22);
Mux2xOutBit Mux2xOutBit_inst34 (
    .I0(Mux2xOutBit_inst34_I0),
    .I1(Mux2xOutBit_inst34_I1),
    .S(Mux2xOutBit_inst34_S),
    .O(Mux2xOutBit_inst34_O)
);
assign Mux2xOutBit_inst35_I0 = Register_inst0_O[35];
assign Mux2xOutBit_inst35_I1 = magma_Bits_8_lshr_inst35_out[0];
assign Mux2xOutBit_inst35_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h23)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h23);
Mux2xOutBit Mux2xOutBit_inst35 (
    .I0(Mux2xOutBit_inst35_I0),
    .I1(Mux2xOutBit_inst35_I1),
    .S(Mux2xOutBit_inst35_S),
    .O(Mux2xOutBit_inst35_O)
);
assign Mux2xOutBit_inst36_I0 = Register_inst0_O[36];
assign Mux2xOutBit_inst36_I1 = magma_Bits_8_lshr_inst36_out[0];
assign Mux2xOutBit_inst36_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h24)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h24);
Mux2xOutBit Mux2xOutBit_inst36 (
    .I0(Mux2xOutBit_inst36_I0),
    .I1(Mux2xOutBit_inst36_I1),
    .S(Mux2xOutBit_inst36_S),
    .O(Mux2xOutBit_inst36_O)
);
assign Mux2xOutBit_inst37_I0 = Register_inst0_O[37];
assign Mux2xOutBit_inst37_I1 = magma_Bits_8_lshr_inst37_out[0];
assign Mux2xOutBit_inst37_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h25)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h25);
Mux2xOutBit Mux2xOutBit_inst37 (
    .I0(Mux2xOutBit_inst37_I0),
    .I1(Mux2xOutBit_inst37_I1),
    .S(Mux2xOutBit_inst37_S),
    .O(Mux2xOutBit_inst37_O)
);
assign Mux2xOutBit_inst38_I0 = Register_inst0_O[38];
assign Mux2xOutBit_inst38_I1 = magma_Bits_8_lshr_inst38_out[0];
assign Mux2xOutBit_inst38_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h26)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h26);
Mux2xOutBit Mux2xOutBit_inst38 (
    .I0(Mux2xOutBit_inst38_I0),
    .I1(Mux2xOutBit_inst38_I1),
    .S(Mux2xOutBit_inst38_S),
    .O(Mux2xOutBit_inst38_O)
);
assign Mux2xOutBit_inst39_I0 = Register_inst0_O[39];
assign Mux2xOutBit_inst39_I1 = magma_Bits_8_lshr_inst39_out[0];
assign Mux2xOutBit_inst39_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h27)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h27);
Mux2xOutBit Mux2xOutBit_inst39 (
    .I0(Mux2xOutBit_inst39_I0),
    .I1(Mux2xOutBit_inst39_I1),
    .S(Mux2xOutBit_inst39_S),
    .O(Mux2xOutBit_inst39_O)
);
assign Mux2xOutBit_inst4_I0 = Register_inst0_O[4];
assign Mux2xOutBit_inst4_I1 = magma_Bits_8_lshr_inst4_out[0];
assign Mux2xOutBit_inst4_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h04)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h04);
Mux2xOutBit Mux2xOutBit_inst4 (
    .I0(Mux2xOutBit_inst4_I0),
    .I1(Mux2xOutBit_inst4_I1),
    .S(Mux2xOutBit_inst4_S),
    .O(Mux2xOutBit_inst4_O)
);
assign Mux2xOutBit_inst40_I0 = Register_inst0_O[40];
assign Mux2xOutBit_inst40_I1 = magma_Bits_8_lshr_inst40_out[0];
assign Mux2xOutBit_inst40_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h28)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h28);
Mux2xOutBit Mux2xOutBit_inst40 (
    .I0(Mux2xOutBit_inst40_I0),
    .I1(Mux2xOutBit_inst40_I1),
    .S(Mux2xOutBit_inst40_S),
    .O(Mux2xOutBit_inst40_O)
);
assign Mux2xOutBit_inst41_I0 = Register_inst0_O[41];
assign Mux2xOutBit_inst41_I1 = magma_Bits_8_lshr_inst41_out[0];
assign Mux2xOutBit_inst41_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h29)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h29);
Mux2xOutBit Mux2xOutBit_inst41 (
    .I0(Mux2xOutBit_inst41_I0),
    .I1(Mux2xOutBit_inst41_I1),
    .S(Mux2xOutBit_inst41_S),
    .O(Mux2xOutBit_inst41_O)
);
assign Mux2xOutBit_inst42_I0 = Register_inst0_O[42];
assign Mux2xOutBit_inst42_I1 = magma_Bits_8_lshr_inst42_out[0];
assign Mux2xOutBit_inst42_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h2a)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2a);
Mux2xOutBit Mux2xOutBit_inst42 (
    .I0(Mux2xOutBit_inst42_I0),
    .I1(Mux2xOutBit_inst42_I1),
    .S(Mux2xOutBit_inst42_S),
    .O(Mux2xOutBit_inst42_O)
);
assign Mux2xOutBit_inst43_I0 = Register_inst0_O[43];
assign Mux2xOutBit_inst43_I1 = magma_Bits_8_lshr_inst43_out[0];
assign Mux2xOutBit_inst43_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h2b)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2b);
Mux2xOutBit Mux2xOutBit_inst43 (
    .I0(Mux2xOutBit_inst43_I0),
    .I1(Mux2xOutBit_inst43_I1),
    .S(Mux2xOutBit_inst43_S),
    .O(Mux2xOutBit_inst43_O)
);
assign Mux2xOutBit_inst44_I0 = Register_inst0_O[44];
assign Mux2xOutBit_inst44_I1 = magma_Bits_8_lshr_inst44_out[0];
assign Mux2xOutBit_inst44_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h2c)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2c);
Mux2xOutBit Mux2xOutBit_inst44 (
    .I0(Mux2xOutBit_inst44_I0),
    .I1(Mux2xOutBit_inst44_I1),
    .S(Mux2xOutBit_inst44_S),
    .O(Mux2xOutBit_inst44_O)
);
assign Mux2xOutBit_inst45_I0 = Register_inst0_O[45];
assign Mux2xOutBit_inst45_I1 = magma_Bits_8_lshr_inst45_out[0];
assign Mux2xOutBit_inst45_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h2d)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2d);
Mux2xOutBit Mux2xOutBit_inst45 (
    .I0(Mux2xOutBit_inst45_I0),
    .I1(Mux2xOutBit_inst45_I1),
    .S(Mux2xOutBit_inst45_S),
    .O(Mux2xOutBit_inst45_O)
);
assign Mux2xOutBit_inst46_I0 = Register_inst0_O[46];
assign Mux2xOutBit_inst46_I1 = magma_Bits_8_lshr_inst46_out[0];
assign Mux2xOutBit_inst46_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h2e)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2e);
Mux2xOutBit Mux2xOutBit_inst46 (
    .I0(Mux2xOutBit_inst46_I0),
    .I1(Mux2xOutBit_inst46_I1),
    .S(Mux2xOutBit_inst46_S),
    .O(Mux2xOutBit_inst46_O)
);
assign Mux2xOutBit_inst47_I0 = Register_inst0_O[47];
assign Mux2xOutBit_inst47_I1 = magma_Bits_8_lshr_inst47_out[0];
assign Mux2xOutBit_inst47_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h2f)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2f);
Mux2xOutBit Mux2xOutBit_inst47 (
    .I0(Mux2xOutBit_inst47_I0),
    .I1(Mux2xOutBit_inst47_I1),
    .S(Mux2xOutBit_inst47_S),
    .O(Mux2xOutBit_inst47_O)
);
assign Mux2xOutBit_inst48_I0 = Register_inst0_O[48];
assign Mux2xOutBit_inst48_I1 = magma_Bits_8_lshr_inst48_out[0];
assign Mux2xOutBit_inst48_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h30)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h30);
Mux2xOutBit Mux2xOutBit_inst48 (
    .I0(Mux2xOutBit_inst48_I0),
    .I1(Mux2xOutBit_inst48_I1),
    .S(Mux2xOutBit_inst48_S),
    .O(Mux2xOutBit_inst48_O)
);
assign Mux2xOutBit_inst49_I0 = Register_inst0_O[49];
assign Mux2xOutBit_inst49_I1 = magma_Bits_8_lshr_inst49_out[0];
assign Mux2xOutBit_inst49_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h31)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h31);
Mux2xOutBit Mux2xOutBit_inst49 (
    .I0(Mux2xOutBit_inst49_I0),
    .I1(Mux2xOutBit_inst49_I1),
    .S(Mux2xOutBit_inst49_S),
    .O(Mux2xOutBit_inst49_O)
);
assign Mux2xOutBit_inst5_I0 = Register_inst0_O[5];
assign Mux2xOutBit_inst5_I1 = magma_Bits_8_lshr_inst5_out[0];
assign Mux2xOutBit_inst5_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h05)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h05);
Mux2xOutBit Mux2xOutBit_inst5 (
    .I0(Mux2xOutBit_inst5_I0),
    .I1(Mux2xOutBit_inst5_I1),
    .S(Mux2xOutBit_inst5_S),
    .O(Mux2xOutBit_inst5_O)
);
assign Mux2xOutBit_inst50_I0 = Register_inst0_O[50];
assign Mux2xOutBit_inst50_I1 = magma_Bits_8_lshr_inst50_out[0];
assign Mux2xOutBit_inst50_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h32)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h32);
Mux2xOutBit Mux2xOutBit_inst50 (
    .I0(Mux2xOutBit_inst50_I0),
    .I1(Mux2xOutBit_inst50_I1),
    .S(Mux2xOutBit_inst50_S),
    .O(Mux2xOutBit_inst50_O)
);
assign Mux2xOutBit_inst51_I0 = Register_inst0_O[51];
assign Mux2xOutBit_inst51_I1 = magma_Bits_8_lshr_inst51_out[0];
assign Mux2xOutBit_inst51_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h33)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h33);
Mux2xOutBit Mux2xOutBit_inst51 (
    .I0(Mux2xOutBit_inst51_I0),
    .I1(Mux2xOutBit_inst51_I1),
    .S(Mux2xOutBit_inst51_S),
    .O(Mux2xOutBit_inst51_O)
);
assign Mux2xOutBit_inst52_I0 = Register_inst0_O[52];
assign Mux2xOutBit_inst52_I1 = magma_Bits_8_lshr_inst52_out[0];
assign Mux2xOutBit_inst52_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h34)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h34);
Mux2xOutBit Mux2xOutBit_inst52 (
    .I0(Mux2xOutBit_inst52_I0),
    .I1(Mux2xOutBit_inst52_I1),
    .S(Mux2xOutBit_inst52_S),
    .O(Mux2xOutBit_inst52_O)
);
assign Mux2xOutBit_inst53_I0 = Register_inst0_O[53];
assign Mux2xOutBit_inst53_I1 = magma_Bits_8_lshr_inst53_out[0];
assign Mux2xOutBit_inst53_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h35)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h35);
Mux2xOutBit Mux2xOutBit_inst53 (
    .I0(Mux2xOutBit_inst53_I0),
    .I1(Mux2xOutBit_inst53_I1),
    .S(Mux2xOutBit_inst53_S),
    .O(Mux2xOutBit_inst53_O)
);
assign Mux2xOutBit_inst54_I0 = Register_inst0_O[54];
assign Mux2xOutBit_inst54_I1 = magma_Bits_8_lshr_inst54_out[0];
assign Mux2xOutBit_inst54_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h36)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h36);
Mux2xOutBit Mux2xOutBit_inst54 (
    .I0(Mux2xOutBit_inst54_I0),
    .I1(Mux2xOutBit_inst54_I1),
    .S(Mux2xOutBit_inst54_S),
    .O(Mux2xOutBit_inst54_O)
);
assign Mux2xOutBit_inst55_I0 = Register_inst0_O[55];
assign Mux2xOutBit_inst55_I1 = magma_Bits_8_lshr_inst55_out[0];
assign Mux2xOutBit_inst55_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h37)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h37);
Mux2xOutBit Mux2xOutBit_inst55 (
    .I0(Mux2xOutBit_inst55_I0),
    .I1(Mux2xOutBit_inst55_I1),
    .S(Mux2xOutBit_inst55_S),
    .O(Mux2xOutBit_inst55_O)
);
assign Mux2xOutBit_inst56_I0 = Register_inst0_O[56];
assign Mux2xOutBit_inst56_I1 = magma_Bits_8_lshr_inst56_out[0];
assign Mux2xOutBit_inst56_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h38)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h38);
Mux2xOutBit Mux2xOutBit_inst56 (
    .I0(Mux2xOutBit_inst56_I0),
    .I1(Mux2xOutBit_inst56_I1),
    .S(Mux2xOutBit_inst56_S),
    .O(Mux2xOutBit_inst56_O)
);
assign Mux2xOutBit_inst57_I0 = Register_inst0_O[57];
assign Mux2xOutBit_inst57_I1 = magma_Bits_8_lshr_inst57_out[0];
assign Mux2xOutBit_inst57_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h39)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h39);
Mux2xOutBit Mux2xOutBit_inst57 (
    .I0(Mux2xOutBit_inst57_I0),
    .I1(Mux2xOutBit_inst57_I1),
    .S(Mux2xOutBit_inst57_S),
    .O(Mux2xOutBit_inst57_O)
);
assign Mux2xOutBit_inst58_I0 = Register_inst0_O[58];
assign Mux2xOutBit_inst58_I1 = magma_Bits_8_lshr_inst58_out[0];
assign Mux2xOutBit_inst58_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h3a)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3a);
Mux2xOutBit Mux2xOutBit_inst58 (
    .I0(Mux2xOutBit_inst58_I0),
    .I1(Mux2xOutBit_inst58_I1),
    .S(Mux2xOutBit_inst58_S),
    .O(Mux2xOutBit_inst58_O)
);
assign Mux2xOutBit_inst59_I0 = Register_inst0_O[59];
assign Mux2xOutBit_inst59_I1 = magma_Bits_8_lshr_inst59_out[0];
assign Mux2xOutBit_inst59_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h3b)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3b);
Mux2xOutBit Mux2xOutBit_inst59 (
    .I0(Mux2xOutBit_inst59_I0),
    .I1(Mux2xOutBit_inst59_I1),
    .S(Mux2xOutBit_inst59_S),
    .O(Mux2xOutBit_inst59_O)
);
assign Mux2xOutBit_inst6_I0 = Register_inst0_O[6];
assign Mux2xOutBit_inst6_I1 = magma_Bits_8_lshr_inst6_out[0];
assign Mux2xOutBit_inst6_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h06)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h06);
Mux2xOutBit Mux2xOutBit_inst6 (
    .I0(Mux2xOutBit_inst6_I0),
    .I1(Mux2xOutBit_inst6_I1),
    .S(Mux2xOutBit_inst6_S),
    .O(Mux2xOutBit_inst6_O)
);
assign Mux2xOutBit_inst60_I0 = Register_inst0_O[60];
assign Mux2xOutBit_inst60_I1 = magma_Bits_8_lshr_inst60_out[0];
assign Mux2xOutBit_inst60_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h3c)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3c);
Mux2xOutBit Mux2xOutBit_inst60 (
    .I0(Mux2xOutBit_inst60_I0),
    .I1(Mux2xOutBit_inst60_I1),
    .S(Mux2xOutBit_inst60_S),
    .O(Mux2xOutBit_inst60_O)
);
assign Mux2xOutBit_inst61_I0 = Register_inst0_O[61];
assign Mux2xOutBit_inst61_I1 = magma_Bits_8_lshr_inst61_out[0];
assign Mux2xOutBit_inst61_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h3d)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3d);
Mux2xOutBit Mux2xOutBit_inst61 (
    .I0(Mux2xOutBit_inst61_I0),
    .I1(Mux2xOutBit_inst61_I1),
    .S(Mux2xOutBit_inst61_S),
    .O(Mux2xOutBit_inst61_O)
);
assign Mux2xOutBit_inst62_I0 = Register_inst0_O[62];
assign Mux2xOutBit_inst62_I1 = magma_Bits_8_lshr_inst62_out[0];
assign Mux2xOutBit_inst62_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h3e)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3e);
Mux2xOutBit Mux2xOutBit_inst62 (
    .I0(Mux2xOutBit_inst62_I0),
    .I1(Mux2xOutBit_inst62_I1),
    .S(Mux2xOutBit_inst62_S),
    .O(Mux2xOutBit_inst62_O)
);
assign Mux2xOutBit_inst63_I0 = Register_inst0_O[63];
assign Mux2xOutBit_inst63_I1 = magma_Bits_8_lshr_inst63_out[0];
assign Mux2xOutBit_inst63_S = 1'b1 & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3f);
Mux2xOutBit Mux2xOutBit_inst63 (
    .I0(Mux2xOutBit_inst63_I0),
    .I1(Mux2xOutBit_inst63_I1),
    .S(Mux2xOutBit_inst63_S),
    .O(Mux2xOutBit_inst63_O)
);
assign Mux2xOutBit_inst7_I0 = Register_inst0_O[7];
assign Mux2xOutBit_inst7_I1 = magma_Bits_8_lshr_inst7_out[0];
assign Mux2xOutBit_inst7_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h07)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h07);
Mux2xOutBit Mux2xOutBit_inst7 (
    .I0(Mux2xOutBit_inst7_I0),
    .I1(Mux2xOutBit_inst7_I1),
    .S(Mux2xOutBit_inst7_S),
    .O(Mux2xOutBit_inst7_O)
);
assign Mux2xOutBit_inst8_I0 = Register_inst0_O[8];
assign Mux2xOutBit_inst8_I1 = magma_Bits_8_lshr_inst8_out[0];
assign Mux2xOutBit_inst8_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h08)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h08);
Mux2xOutBit Mux2xOutBit_inst8 (
    .I0(Mux2xOutBit_inst8_I0),
    .I1(Mux2xOutBit_inst8_I1),
    .S(Mux2xOutBit_inst8_S),
    .O(Mux2xOutBit_inst8_O)
);
assign Mux2xOutBit_inst9_I0 = Register_inst0_O[9];
assign Mux2xOutBit_inst9_I1 = magma_Bits_8_lshr_inst9_out[0];
assign Mux2xOutBit_inst9_S = (1'b1 & (magma_Bits_6_mul_inst1_out <= 6'h09)) & ((6'((6'(magma_Bits_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h09);
Mux2xOutBit Mux2xOutBit_inst9 (
    .I0(Mux2xOutBit_inst9_I0),
    .I1(Mux2xOutBit_inst9_I1),
    .S(Mux2xOutBit_inst9_S),
    .O(Mux2xOutBit_inst9_O)
);
assign Mux56xOutBits8_inst0_I0 = Register_inst0_O[7:0];
assign Mux56xOutBits8_inst0_I1 = Register_inst0_O[8:1];
assign Mux56xOutBits8_inst0_I2 = Register_inst0_O[9:2];
assign Mux56xOutBits8_inst0_I3 = Register_inst0_O[10:3];
assign Mux56xOutBits8_inst0_I4 = Register_inst0_O[11:4];
assign Mux56xOutBits8_inst0_I5 = Register_inst0_O[12:5];
assign Mux56xOutBits8_inst0_I6 = Register_inst0_O[13:6];
assign Mux56xOutBits8_inst0_I7 = Register_inst0_O[14:7];
assign Mux56xOutBits8_inst0_I8 = Register_inst0_O[15:8];
assign Mux56xOutBits8_inst0_I9 = Register_inst0_O[16:9];
assign Mux56xOutBits8_inst0_I10 = Register_inst0_O[17:10];
assign Mux56xOutBits8_inst0_I11 = Register_inst0_O[18:11];
assign Mux56xOutBits8_inst0_I12 = Register_inst0_O[19:12];
assign Mux56xOutBits8_inst0_I13 = Register_inst0_O[20:13];
assign Mux56xOutBits8_inst0_I14 = Register_inst0_O[21:14];
assign Mux56xOutBits8_inst0_I15 = Register_inst0_O[22:15];
assign Mux56xOutBits8_inst0_I16 = Register_inst0_O[23:16];
assign Mux56xOutBits8_inst0_I17 = Register_inst0_O[24:17];
assign Mux56xOutBits8_inst0_I18 = Register_inst0_O[25:18];
assign Mux56xOutBits8_inst0_I19 = Register_inst0_O[26:19];
assign Mux56xOutBits8_inst0_I20 = Register_inst0_O[27:20];
assign Mux56xOutBits8_inst0_I21 = Register_inst0_O[28:21];
assign Mux56xOutBits8_inst0_I22 = Register_inst0_O[29:22];
assign Mux56xOutBits8_inst0_I23 = Register_inst0_O[30:23];
assign Mux56xOutBits8_inst0_I24 = Register_inst0_O[31:24];
assign Mux56xOutBits8_inst0_I25 = Register_inst0_O[32:25];
assign Mux56xOutBits8_inst0_I26 = Register_inst0_O[33:26];
assign Mux56xOutBits8_inst0_I27 = Register_inst0_O[34:27];
assign Mux56xOutBits8_inst0_I28 = Register_inst0_O[35:28];
assign Mux56xOutBits8_inst0_I29 = Register_inst0_O[36:29];
assign Mux56xOutBits8_inst0_I30 = Register_inst0_O[37:30];
assign Mux56xOutBits8_inst0_I31 = Register_inst0_O[38:31];
assign Mux56xOutBits8_inst0_I32 = Register_inst0_O[39:32];
assign Mux56xOutBits8_inst0_I33 = Register_inst0_O[40:33];
assign Mux56xOutBits8_inst0_I34 = Register_inst0_O[41:34];
assign Mux56xOutBits8_inst0_I35 = Register_inst0_O[42:35];
assign Mux56xOutBits8_inst0_I36 = Register_inst0_O[43:36];
assign Mux56xOutBits8_inst0_I37 = Register_inst0_O[44:37];
assign Mux56xOutBits8_inst0_I38 = Register_inst0_O[45:38];
assign Mux56xOutBits8_inst0_I39 = Register_inst0_O[46:39];
assign Mux56xOutBits8_inst0_I40 = Register_inst0_O[47:40];
assign Mux56xOutBits8_inst0_I41 = Register_inst0_O[48:41];
assign Mux56xOutBits8_inst0_I42 = Register_inst0_O[49:42];
assign Mux56xOutBits8_inst0_I43 = Register_inst0_O[50:43];
assign Mux56xOutBits8_inst0_I44 = Register_inst0_O[51:44];
assign Mux56xOutBits8_inst0_I45 = Register_inst0_O[52:45];
assign Mux56xOutBits8_inst0_I46 = Register_inst0_O[53:46];
assign Mux56xOutBits8_inst0_I47 = Register_inst0_O[54:47];
assign Mux56xOutBits8_inst0_I48 = Register_inst0_O[55:48];
assign Mux56xOutBits8_inst0_I49 = Register_inst0_O[56:49];
assign Mux56xOutBits8_inst0_I50 = Register_inst0_O[57:50];
assign Mux56xOutBits8_inst0_I51 = Register_inst0_O[58:51];
assign Mux56xOutBits8_inst0_I52 = Register_inst0_O[59:52];
assign Mux56xOutBits8_inst0_I53 = Register_inst0_O[60:53];
assign Mux56xOutBits8_inst0_I54 = Register_inst0_O[61:54];
assign Mux56xOutBits8_inst0_I55 = Register_inst0_O[62:55];
assign Mux56xOutBits8_inst0_S = 6'(({1'b0,1'b0,1'b0,read_addr[2:0]}) * 6'h08);
Mux56xOutBits8 Mux56xOutBits8_inst0 (
    .I0(Mux56xOutBits8_inst0_I0),
    .I1(Mux56xOutBits8_inst0_I1),
    .I2(Mux56xOutBits8_inst0_I2),
    .I3(Mux56xOutBits8_inst0_I3),
    .I4(Mux56xOutBits8_inst0_I4),
    .I5(Mux56xOutBits8_inst0_I5),
    .I6(Mux56xOutBits8_inst0_I6),
    .I7(Mux56xOutBits8_inst0_I7),
    .I8(Mux56xOutBits8_inst0_I8),
    .I9(Mux56xOutBits8_inst0_I9),
    .I10(Mux56xOutBits8_inst0_I10),
    .I11(Mux56xOutBits8_inst0_I11),
    .I12(Mux56xOutBits8_inst0_I12),
    .I13(Mux56xOutBits8_inst0_I13),
    .I14(Mux56xOutBits8_inst0_I14),
    .I15(Mux56xOutBits8_inst0_I15),
    .I16(Mux56xOutBits8_inst0_I16),
    .I17(Mux56xOutBits8_inst0_I17),
    .I18(Mux56xOutBits8_inst0_I18),
    .I19(Mux56xOutBits8_inst0_I19),
    .I20(Mux56xOutBits8_inst0_I20),
    .I21(Mux56xOutBits8_inst0_I21),
    .I22(Mux56xOutBits8_inst0_I22),
    .I23(Mux56xOutBits8_inst0_I23),
    .I24(Mux56xOutBits8_inst0_I24),
    .I25(Mux56xOutBits8_inst0_I25),
    .I26(Mux56xOutBits8_inst0_I26),
    .I27(Mux56xOutBits8_inst0_I27),
    .I28(Mux56xOutBits8_inst0_I28),
    .I29(Mux56xOutBits8_inst0_I29),
    .I30(Mux56xOutBits8_inst0_I30),
    .I31(Mux56xOutBits8_inst0_I31),
    .I32(Mux56xOutBits8_inst0_I32),
    .I33(Mux56xOutBits8_inst0_I33),
    .I34(Mux56xOutBits8_inst0_I34),
    .I35(Mux56xOutBits8_inst0_I35),
    .I36(Mux56xOutBits8_inst0_I36),
    .I37(Mux56xOutBits8_inst0_I37),
    .I38(Mux56xOutBits8_inst0_I38),
    .I39(Mux56xOutBits8_inst0_I39),
    .I40(Mux56xOutBits8_inst0_I40),
    .I41(Mux56xOutBits8_inst0_I41),
    .I42(Mux56xOutBits8_inst0_I42),
    .I43(Mux56xOutBits8_inst0_I43),
    .I44(Mux56xOutBits8_inst0_I44),
    .I45(Mux56xOutBits8_inst0_I45),
    .I46(Mux56xOutBits8_inst0_I46),
    .I47(Mux56xOutBits8_inst0_I47),
    .I48(Mux56xOutBits8_inst0_I48),
    .I49(Mux56xOutBits8_inst0_I49),
    .I50(Mux56xOutBits8_inst0_I50),
    .I51(Mux56xOutBits8_inst0_I51),
    .I52(Mux56xOutBits8_inst0_I52),
    .I53(Mux56xOutBits8_inst0_I53),
    .I54(Mux56xOutBits8_inst0_I54),
    .I55(Mux56xOutBits8_inst0_I55),
    .S(Mux56xOutBits8_inst0_S),
    .O(O)
);
assign Register_inst0_I = {Mux2xOutBit_inst63_O,Mux2xOutBit_inst62_O,Mux2xOutBit_inst61_O,Mux2xOutBit_inst60_O,Mux2xOutBit_inst59_O,Mux2xOutBit_inst58_O,Mux2xOutBit_inst57_O,Mux2xOutBit_inst56_O,Mux2xOutBit_inst55_O,Mux2xOutBit_inst54_O,Mux2xOutBit_inst53_O,Mux2xOutBit_inst52_O,Mux2xOutBit_inst51_O,Mux2xOutBit_inst50_O,Mux2xOutBit_inst49_O,Mux2xOutBit_inst48_O,Mux2xOutBit_inst47_O,Mux2xOutBit_inst46_O,Mux2xOutBit_inst45_O,Mux2xOutBit_inst44_O,Mux2xOutBit_inst43_O,Mux2xOutBit_inst42_O,Mux2xOutBit_inst41_O,Mux2xOutBit_inst40_O,Mux2xOutBit_inst39_O,Mux2xOutBit_inst38_O,Mux2xOutBit_inst37_O,Mux2xOutBit_inst36_O,Mux2xOutBit_inst35_O,Mux2xOutBit_inst34_O,Mux2xOutBit_inst33_O,Mux2xOutBit_inst32_O,Mux2xOutBit_inst31_O,Mux2xOutBit_inst30_O,Mux2xOutBit_inst29_O,Mux2xOutBit_inst28_O,Mux2xOutBit_inst27_O,Mux2xOutBit_inst26_O,Mux2xOutBit_inst25_O,Mux2xOutBit_inst24_O,Mux2xOutBit_inst23_O,Mux2xOutBit_inst22_O,Mux2xOutBit_inst21_O,Mux2xOutBit_inst20_O,Mux2xOutBit_inst19_O,Mux2xOutBit_inst18_O,Mux2xOutBit_inst17_O,Mux2xOutBit_inst16_O,Mux2xOutBit_inst15_O,Mux2xOutBit_inst14_O,Mux2xOutBit_inst13_O,Mux2xOutBit_inst12_O,Mux2xOutBit_inst11_O,Mux2xOutBit_inst10_O,Mux2xOutBit_inst9_O,Mux2xOutBit_inst8_O,Mux2xOutBit_inst7_O,Mux2xOutBit_inst6_O,Mux2xOutBit_inst5_O,Mux2xOutBit_inst4_O,Mux2xOutBit_inst3_O,Mux2xOutBit_inst2_O,Mux2xOutBit_inst1_O,Mux2xOutBit_inst0_O};
assign Register_inst0_CLK = CLK;
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(Register_inst0_CLK)
);
assign magma_Bits_6_mul_inst1_out = 6'(({1'b0,1'b0,1'b0,write_addr[2:0]}) * 6'h08);
assign magma_Bits_6_sub_inst0_out = 6'(6'h00 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst10_out = 6'(6'h05 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst100_out = 6'(6'h32 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst102_out = 6'(6'h33 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst104_out = 6'(6'h34 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst106_out = 6'(6'h35 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst108_out = 6'(6'h36 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst110_out = 6'(6'h37 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst112_out = 6'(6'h38 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst114_out = 6'(6'h39 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst116_out = 6'(6'h3a - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst118_out = 6'(6'h3b - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst12_out = 6'(6'h06 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst120_out = 6'(6'h3c - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst122_out = 6'(6'h3d - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst124_out = 6'(6'h3e - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst126_out = 6'(6'h3f - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst14_out = 6'(6'h07 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst16_out = 6'(6'h08 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst18_out = 6'(6'h09 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst2_out = 6'(6'h01 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst20_out = 6'(6'h0a - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst22_out = 6'(6'h0b - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst24_out = 6'(6'h0c - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst26_out = 6'(6'h0d - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst28_out = 6'(6'h0e - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst30_out = 6'(6'h0f - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst32_out = 6'(6'h10 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst34_out = 6'(6'h11 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst36_out = 6'(6'h12 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst38_out = 6'(6'h13 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst4_out = 6'(6'h02 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst40_out = 6'(6'h14 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst42_out = 6'(6'h15 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst44_out = 6'(6'h16 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst46_out = 6'(6'h17 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst48_out = 6'(6'h18 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst50_out = 6'(6'h19 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst52_out = 6'(6'h1a - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst54_out = 6'(6'h1b - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst56_out = 6'(6'h1c - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst58_out = 6'(6'h1d - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst6_out = 6'(6'h03 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst60_out = 6'(6'h1e - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst62_out = 6'(6'h1f - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst64_out = 6'(6'h20 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst66_out = 6'(6'h21 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst68_out = 6'(6'h22 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst70_out = 6'(6'h23 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst72_out = 6'(6'h24 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst74_out = 6'(6'h25 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst76_out = 6'(6'h26 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst78_out = 6'(6'h27 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst8_out = 6'(6'h04 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst80_out = 6'(6'h28 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst82_out = 6'(6'h29 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst84_out = 6'(6'h2a - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst86_out = 6'(6'h2b - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst88_out = 6'(6'h2c - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst90_out = 6'(6'h2d - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst92_out = 6'(6'h2e - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst94_out = 6'(6'h2f - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst96_out = 6'(6'h30 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_6_sub_inst98_out = 6'(6'h31 - magma_Bits_6_mul_inst1_out);
assign magma_Bits_8_lshr_inst0_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst0_out[2:0]});
assign magma_Bits_8_lshr_inst1_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst2_out[2:0]});
assign magma_Bits_8_lshr_inst10_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst20_out[2:0]});
assign magma_Bits_8_lshr_inst11_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst22_out[2:0]});
assign magma_Bits_8_lshr_inst12_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst24_out[2:0]});
assign magma_Bits_8_lshr_inst13_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst26_out[2:0]});
assign magma_Bits_8_lshr_inst14_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst28_out[2:0]});
assign magma_Bits_8_lshr_inst15_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst30_out[2:0]});
assign magma_Bits_8_lshr_inst16_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst32_out[2:0]});
assign magma_Bits_8_lshr_inst17_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst34_out[2:0]});
assign magma_Bits_8_lshr_inst18_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst36_out[2:0]});
assign magma_Bits_8_lshr_inst19_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst38_out[2:0]});
assign magma_Bits_8_lshr_inst2_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst4_out[2:0]});
assign magma_Bits_8_lshr_inst20_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst40_out[2:0]});
assign magma_Bits_8_lshr_inst21_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst42_out[2:0]});
assign magma_Bits_8_lshr_inst22_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst44_out[2:0]});
assign magma_Bits_8_lshr_inst23_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst46_out[2:0]});
assign magma_Bits_8_lshr_inst24_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst48_out[2:0]});
assign magma_Bits_8_lshr_inst25_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst50_out[2:0]});
assign magma_Bits_8_lshr_inst26_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst52_out[2:0]});
assign magma_Bits_8_lshr_inst27_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst54_out[2:0]});
assign magma_Bits_8_lshr_inst28_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst56_out[2:0]});
assign magma_Bits_8_lshr_inst29_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst58_out[2:0]});
assign magma_Bits_8_lshr_inst3_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst6_out[2:0]});
assign magma_Bits_8_lshr_inst30_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst60_out[2:0]});
assign magma_Bits_8_lshr_inst31_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst62_out[2:0]});
assign magma_Bits_8_lshr_inst32_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst64_out[2:0]});
assign magma_Bits_8_lshr_inst33_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst66_out[2:0]});
assign magma_Bits_8_lshr_inst34_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst68_out[2:0]});
assign magma_Bits_8_lshr_inst35_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst70_out[2:0]});
assign magma_Bits_8_lshr_inst36_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst72_out[2:0]});
assign magma_Bits_8_lshr_inst37_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst74_out[2:0]});
assign magma_Bits_8_lshr_inst38_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst76_out[2:0]});
assign magma_Bits_8_lshr_inst39_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst78_out[2:0]});
assign magma_Bits_8_lshr_inst4_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst8_out[2:0]});
assign magma_Bits_8_lshr_inst40_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst80_out[2:0]});
assign magma_Bits_8_lshr_inst41_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst82_out[2:0]});
assign magma_Bits_8_lshr_inst42_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst84_out[2:0]});
assign magma_Bits_8_lshr_inst43_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst86_out[2:0]});
assign magma_Bits_8_lshr_inst44_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst88_out[2:0]});
assign magma_Bits_8_lshr_inst45_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst90_out[2:0]});
assign magma_Bits_8_lshr_inst46_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst92_out[2:0]});
assign magma_Bits_8_lshr_inst47_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst94_out[2:0]});
assign magma_Bits_8_lshr_inst48_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst96_out[2:0]});
assign magma_Bits_8_lshr_inst49_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst98_out[2:0]});
assign magma_Bits_8_lshr_inst5_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst10_out[2:0]});
assign magma_Bits_8_lshr_inst50_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst100_out[2:0]});
assign magma_Bits_8_lshr_inst51_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst102_out[2:0]});
assign magma_Bits_8_lshr_inst52_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst104_out[2:0]});
assign magma_Bits_8_lshr_inst53_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst106_out[2:0]});
assign magma_Bits_8_lshr_inst54_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst108_out[2:0]});
assign magma_Bits_8_lshr_inst55_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst110_out[2:0]});
assign magma_Bits_8_lshr_inst56_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst112_out[2:0]});
assign magma_Bits_8_lshr_inst57_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst114_out[2:0]});
assign magma_Bits_8_lshr_inst58_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst116_out[2:0]});
assign magma_Bits_8_lshr_inst59_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst118_out[2:0]});
assign magma_Bits_8_lshr_inst6_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst12_out[2:0]});
assign magma_Bits_8_lshr_inst60_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst120_out[2:0]});
assign magma_Bits_8_lshr_inst61_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst122_out[2:0]});
assign magma_Bits_8_lshr_inst62_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst124_out[2:0]});
assign magma_Bits_8_lshr_inst63_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst126_out[2:0]});
assign magma_Bits_8_lshr_inst7_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst14_out[2:0]});
assign magma_Bits_8_lshr_inst8_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst16_out[2:0]});
assign magma_Bits_8_lshr_inst9_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_Bits_6_sub_inst18_out[2:0]});
endmodule

