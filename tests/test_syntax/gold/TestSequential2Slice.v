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
coreir_reg #(
    .clk_posedge(1'b1),
    .init(64'h0000000000000000),
    .width(64)
) reg_P64_inst0 (
    .clk(CLK),
    .in(I),
    .out(O)
);
endmodule

module Mux56xBits8 (
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

module Mux2xBit (
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
wire Mux2xBit_inst0_O;
wire Mux2xBit_inst1_O;
wire Mux2xBit_inst10_O;
wire Mux2xBit_inst11_O;
wire Mux2xBit_inst12_O;
wire Mux2xBit_inst13_O;
wire Mux2xBit_inst14_O;
wire Mux2xBit_inst15_O;
wire Mux2xBit_inst16_O;
wire Mux2xBit_inst17_O;
wire Mux2xBit_inst18_O;
wire Mux2xBit_inst19_O;
wire Mux2xBit_inst2_O;
wire Mux2xBit_inst20_O;
wire Mux2xBit_inst21_O;
wire Mux2xBit_inst22_O;
wire Mux2xBit_inst23_O;
wire Mux2xBit_inst24_O;
wire Mux2xBit_inst25_O;
wire Mux2xBit_inst26_O;
wire Mux2xBit_inst27_O;
wire Mux2xBit_inst28_O;
wire Mux2xBit_inst29_O;
wire Mux2xBit_inst3_O;
wire Mux2xBit_inst30_O;
wire Mux2xBit_inst31_O;
wire Mux2xBit_inst32_O;
wire Mux2xBit_inst33_O;
wire Mux2xBit_inst34_O;
wire Mux2xBit_inst35_O;
wire Mux2xBit_inst36_O;
wire Mux2xBit_inst37_O;
wire Mux2xBit_inst38_O;
wire Mux2xBit_inst39_O;
wire Mux2xBit_inst4_O;
wire Mux2xBit_inst40_O;
wire Mux2xBit_inst41_O;
wire Mux2xBit_inst42_O;
wire Mux2xBit_inst43_O;
wire Mux2xBit_inst44_O;
wire Mux2xBit_inst45_O;
wire Mux2xBit_inst46_O;
wire Mux2xBit_inst47_O;
wire Mux2xBit_inst48_O;
wire Mux2xBit_inst49_O;
wire Mux2xBit_inst5_O;
wire Mux2xBit_inst50_O;
wire Mux2xBit_inst51_O;
wire Mux2xBit_inst52_O;
wire Mux2xBit_inst53_O;
wire Mux2xBit_inst54_O;
wire Mux2xBit_inst55_O;
wire Mux2xBit_inst56_O;
wire Mux2xBit_inst57_O;
wire Mux2xBit_inst58_O;
wire Mux2xBit_inst59_O;
wire Mux2xBit_inst6_O;
wire Mux2xBit_inst60_O;
wire Mux2xBit_inst61_O;
wire Mux2xBit_inst62_O;
wire Mux2xBit_inst63_O;
wire Mux2xBit_inst7_O;
wire Mux2xBit_inst8_O;
wire Mux2xBit_inst9_O;
wire [63:0] Register_inst0_O;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst10_out;
wire magma_Bit_and_inst100_out;
wire magma_Bit_and_inst102_out;
wire magma_Bit_and_inst104_out;
wire magma_Bit_and_inst106_out;
wire magma_Bit_and_inst108_out;
wire magma_Bit_and_inst110_out;
wire magma_Bit_and_inst112_out;
wire magma_Bit_and_inst114_out;
wire magma_Bit_and_inst116_out;
wire magma_Bit_and_inst118_out;
wire magma_Bit_and_inst12_out;
wire magma_Bit_and_inst120_out;
wire magma_Bit_and_inst122_out;
wire magma_Bit_and_inst124_out;
wire magma_Bit_and_inst125_out;
wire magma_Bit_and_inst14_out;
wire magma_Bit_and_inst16_out;
wire magma_Bit_and_inst18_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst20_out;
wire magma_Bit_and_inst22_out;
wire magma_Bit_and_inst24_out;
wire magma_Bit_and_inst26_out;
wire magma_Bit_and_inst28_out;
wire magma_Bit_and_inst30_out;
wire magma_Bit_and_inst32_out;
wire magma_Bit_and_inst34_out;
wire magma_Bit_and_inst36_out;
wire magma_Bit_and_inst38_out;
wire magma_Bit_and_inst4_out;
wire magma_Bit_and_inst40_out;
wire magma_Bit_and_inst42_out;
wire magma_Bit_and_inst44_out;
wire magma_Bit_and_inst46_out;
wire magma_Bit_and_inst48_out;
wire magma_Bit_and_inst50_out;
wire magma_Bit_and_inst52_out;
wire magma_Bit_and_inst54_out;
wire magma_Bit_and_inst56_out;
wire magma_Bit_and_inst58_out;
wire magma_Bit_and_inst6_out;
wire magma_Bit_and_inst60_out;
wire magma_Bit_and_inst62_out;
wire magma_Bit_and_inst64_out;
wire magma_Bit_and_inst66_out;
wire magma_Bit_and_inst68_out;
wire magma_Bit_and_inst70_out;
wire magma_Bit_and_inst72_out;
wire magma_Bit_and_inst74_out;
wire magma_Bit_and_inst76_out;
wire magma_Bit_and_inst78_out;
wire magma_Bit_and_inst8_out;
wire magma_Bit_and_inst80_out;
wire magma_Bit_and_inst82_out;
wire magma_Bit_and_inst84_out;
wire magma_Bit_and_inst86_out;
wire magma_Bit_and_inst88_out;
wire magma_Bit_and_inst90_out;
wire magma_Bit_and_inst92_out;
wire magma_Bit_and_inst94_out;
wire magma_Bit_and_inst96_out;
wire magma_Bit_and_inst98_out;
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
wire [5:0] magma_UInt_6_mul_inst0_out;
wire [5:0] magma_UInt_6_mul_inst1_out;
wire [5:0] magma_UInt_6_sub_inst0_out;
wire [5:0] magma_UInt_6_sub_inst10_out;
wire [5:0] magma_UInt_6_sub_inst100_out;
wire [5:0] magma_UInt_6_sub_inst102_out;
wire [5:0] magma_UInt_6_sub_inst104_out;
wire [5:0] magma_UInt_6_sub_inst106_out;
wire [5:0] magma_UInt_6_sub_inst108_out;
wire [5:0] magma_UInt_6_sub_inst110_out;
wire [5:0] magma_UInt_6_sub_inst112_out;
wire [5:0] magma_UInt_6_sub_inst114_out;
wire [5:0] magma_UInt_6_sub_inst116_out;
wire [5:0] magma_UInt_6_sub_inst118_out;
wire [5:0] magma_UInt_6_sub_inst12_out;
wire [5:0] magma_UInt_6_sub_inst120_out;
wire [5:0] magma_UInt_6_sub_inst122_out;
wire [5:0] magma_UInt_6_sub_inst124_out;
wire [5:0] magma_UInt_6_sub_inst126_out;
wire [5:0] magma_UInt_6_sub_inst14_out;
wire [5:0] magma_UInt_6_sub_inst16_out;
wire [5:0] magma_UInt_6_sub_inst18_out;
wire [5:0] magma_UInt_6_sub_inst2_out;
wire [5:0] magma_UInt_6_sub_inst20_out;
wire [5:0] magma_UInt_6_sub_inst22_out;
wire [5:0] magma_UInt_6_sub_inst24_out;
wire [5:0] magma_UInt_6_sub_inst26_out;
wire [5:0] magma_UInt_6_sub_inst28_out;
wire [5:0] magma_UInt_6_sub_inst30_out;
wire [5:0] magma_UInt_6_sub_inst32_out;
wire [5:0] magma_UInt_6_sub_inst34_out;
wire [5:0] magma_UInt_6_sub_inst36_out;
wire [5:0] magma_UInt_6_sub_inst38_out;
wire [5:0] magma_UInt_6_sub_inst4_out;
wire [5:0] magma_UInt_6_sub_inst40_out;
wire [5:0] magma_UInt_6_sub_inst42_out;
wire [5:0] magma_UInt_6_sub_inst44_out;
wire [5:0] magma_UInt_6_sub_inst46_out;
wire [5:0] magma_UInt_6_sub_inst48_out;
wire [5:0] magma_UInt_6_sub_inst50_out;
wire [5:0] magma_UInt_6_sub_inst52_out;
wire [5:0] magma_UInt_6_sub_inst54_out;
wire [5:0] magma_UInt_6_sub_inst56_out;
wire [5:0] magma_UInt_6_sub_inst58_out;
wire [5:0] magma_UInt_6_sub_inst6_out;
wire [5:0] magma_UInt_6_sub_inst60_out;
wire [5:0] magma_UInt_6_sub_inst62_out;
wire [5:0] magma_UInt_6_sub_inst64_out;
wire [5:0] magma_UInt_6_sub_inst66_out;
wire [5:0] magma_UInt_6_sub_inst68_out;
wire [5:0] magma_UInt_6_sub_inst70_out;
wire [5:0] magma_UInt_6_sub_inst72_out;
wire [5:0] magma_UInt_6_sub_inst74_out;
wire [5:0] magma_UInt_6_sub_inst76_out;
wire [5:0] magma_UInt_6_sub_inst78_out;
wire [5:0] magma_UInt_6_sub_inst8_out;
wire [5:0] magma_UInt_6_sub_inst80_out;
wire [5:0] magma_UInt_6_sub_inst82_out;
wire [5:0] magma_UInt_6_sub_inst84_out;
wire [5:0] magma_UInt_6_sub_inst86_out;
wire [5:0] magma_UInt_6_sub_inst88_out;
wire [5:0] magma_UInt_6_sub_inst90_out;
wire [5:0] magma_UInt_6_sub_inst92_out;
wire [5:0] magma_UInt_6_sub_inst94_out;
wire [5:0] magma_UInt_6_sub_inst96_out;
wire [5:0] magma_UInt_6_sub_inst98_out;
Mux2xBit Mux2xBit_inst0 (
    .I0(Register_inst0_O[0]),
    .I1(magma_Bits_8_lshr_inst0_out[0]),
    .S(magma_Bit_and_inst0_out),
    .O(Mux2xBit_inst0_O)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(Register_inst0_O[1]),
    .I1(magma_Bits_8_lshr_inst1_out[0]),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xBit_inst1_O)
);
Mux2xBit Mux2xBit_inst10 (
    .I0(Register_inst0_O[10]),
    .I1(magma_Bits_8_lshr_inst10_out[0]),
    .S(magma_Bit_and_inst20_out),
    .O(Mux2xBit_inst10_O)
);
Mux2xBit Mux2xBit_inst11 (
    .I0(Register_inst0_O[11]),
    .I1(magma_Bits_8_lshr_inst11_out[0]),
    .S(magma_Bit_and_inst22_out),
    .O(Mux2xBit_inst11_O)
);
Mux2xBit Mux2xBit_inst12 (
    .I0(Register_inst0_O[12]),
    .I1(magma_Bits_8_lshr_inst12_out[0]),
    .S(magma_Bit_and_inst24_out),
    .O(Mux2xBit_inst12_O)
);
Mux2xBit Mux2xBit_inst13 (
    .I0(Register_inst0_O[13]),
    .I1(magma_Bits_8_lshr_inst13_out[0]),
    .S(magma_Bit_and_inst26_out),
    .O(Mux2xBit_inst13_O)
);
Mux2xBit Mux2xBit_inst14 (
    .I0(Register_inst0_O[14]),
    .I1(magma_Bits_8_lshr_inst14_out[0]),
    .S(magma_Bit_and_inst28_out),
    .O(Mux2xBit_inst14_O)
);
Mux2xBit Mux2xBit_inst15 (
    .I0(Register_inst0_O[15]),
    .I1(magma_Bits_8_lshr_inst15_out[0]),
    .S(magma_Bit_and_inst30_out),
    .O(Mux2xBit_inst15_O)
);
Mux2xBit Mux2xBit_inst16 (
    .I0(Register_inst0_O[16]),
    .I1(magma_Bits_8_lshr_inst16_out[0]),
    .S(magma_Bit_and_inst32_out),
    .O(Mux2xBit_inst16_O)
);
Mux2xBit Mux2xBit_inst17 (
    .I0(Register_inst0_O[17]),
    .I1(magma_Bits_8_lshr_inst17_out[0]),
    .S(magma_Bit_and_inst34_out),
    .O(Mux2xBit_inst17_O)
);
Mux2xBit Mux2xBit_inst18 (
    .I0(Register_inst0_O[18]),
    .I1(magma_Bits_8_lshr_inst18_out[0]),
    .S(magma_Bit_and_inst36_out),
    .O(Mux2xBit_inst18_O)
);
Mux2xBit Mux2xBit_inst19 (
    .I0(Register_inst0_O[19]),
    .I1(magma_Bits_8_lshr_inst19_out[0]),
    .S(magma_Bit_and_inst38_out),
    .O(Mux2xBit_inst19_O)
);
Mux2xBit Mux2xBit_inst2 (
    .I0(Register_inst0_O[2]),
    .I1(magma_Bits_8_lshr_inst2_out[0]),
    .S(magma_Bit_and_inst4_out),
    .O(Mux2xBit_inst2_O)
);
Mux2xBit Mux2xBit_inst20 (
    .I0(Register_inst0_O[20]),
    .I1(magma_Bits_8_lshr_inst20_out[0]),
    .S(magma_Bit_and_inst40_out),
    .O(Mux2xBit_inst20_O)
);
Mux2xBit Mux2xBit_inst21 (
    .I0(Register_inst0_O[21]),
    .I1(magma_Bits_8_lshr_inst21_out[0]),
    .S(magma_Bit_and_inst42_out),
    .O(Mux2xBit_inst21_O)
);
Mux2xBit Mux2xBit_inst22 (
    .I0(Register_inst0_O[22]),
    .I1(magma_Bits_8_lshr_inst22_out[0]),
    .S(magma_Bit_and_inst44_out),
    .O(Mux2xBit_inst22_O)
);
Mux2xBit Mux2xBit_inst23 (
    .I0(Register_inst0_O[23]),
    .I1(magma_Bits_8_lshr_inst23_out[0]),
    .S(magma_Bit_and_inst46_out),
    .O(Mux2xBit_inst23_O)
);
Mux2xBit Mux2xBit_inst24 (
    .I0(Register_inst0_O[24]),
    .I1(magma_Bits_8_lshr_inst24_out[0]),
    .S(magma_Bit_and_inst48_out),
    .O(Mux2xBit_inst24_O)
);
Mux2xBit Mux2xBit_inst25 (
    .I0(Register_inst0_O[25]),
    .I1(magma_Bits_8_lshr_inst25_out[0]),
    .S(magma_Bit_and_inst50_out),
    .O(Mux2xBit_inst25_O)
);
Mux2xBit Mux2xBit_inst26 (
    .I0(Register_inst0_O[26]),
    .I1(magma_Bits_8_lshr_inst26_out[0]),
    .S(magma_Bit_and_inst52_out),
    .O(Mux2xBit_inst26_O)
);
Mux2xBit Mux2xBit_inst27 (
    .I0(Register_inst0_O[27]),
    .I1(magma_Bits_8_lshr_inst27_out[0]),
    .S(magma_Bit_and_inst54_out),
    .O(Mux2xBit_inst27_O)
);
Mux2xBit Mux2xBit_inst28 (
    .I0(Register_inst0_O[28]),
    .I1(magma_Bits_8_lshr_inst28_out[0]),
    .S(magma_Bit_and_inst56_out),
    .O(Mux2xBit_inst28_O)
);
Mux2xBit Mux2xBit_inst29 (
    .I0(Register_inst0_O[29]),
    .I1(magma_Bits_8_lshr_inst29_out[0]),
    .S(magma_Bit_and_inst58_out),
    .O(Mux2xBit_inst29_O)
);
Mux2xBit Mux2xBit_inst3 (
    .I0(Register_inst0_O[3]),
    .I1(magma_Bits_8_lshr_inst3_out[0]),
    .S(magma_Bit_and_inst6_out),
    .O(Mux2xBit_inst3_O)
);
Mux2xBit Mux2xBit_inst30 (
    .I0(Register_inst0_O[30]),
    .I1(magma_Bits_8_lshr_inst30_out[0]),
    .S(magma_Bit_and_inst60_out),
    .O(Mux2xBit_inst30_O)
);
Mux2xBit Mux2xBit_inst31 (
    .I0(Register_inst0_O[31]),
    .I1(magma_Bits_8_lshr_inst31_out[0]),
    .S(magma_Bit_and_inst62_out),
    .O(Mux2xBit_inst31_O)
);
Mux2xBit Mux2xBit_inst32 (
    .I0(Register_inst0_O[32]),
    .I1(magma_Bits_8_lshr_inst32_out[0]),
    .S(magma_Bit_and_inst64_out),
    .O(Mux2xBit_inst32_O)
);
Mux2xBit Mux2xBit_inst33 (
    .I0(Register_inst0_O[33]),
    .I1(magma_Bits_8_lshr_inst33_out[0]),
    .S(magma_Bit_and_inst66_out),
    .O(Mux2xBit_inst33_O)
);
Mux2xBit Mux2xBit_inst34 (
    .I0(Register_inst0_O[34]),
    .I1(magma_Bits_8_lshr_inst34_out[0]),
    .S(magma_Bit_and_inst68_out),
    .O(Mux2xBit_inst34_O)
);
Mux2xBit Mux2xBit_inst35 (
    .I0(Register_inst0_O[35]),
    .I1(magma_Bits_8_lshr_inst35_out[0]),
    .S(magma_Bit_and_inst70_out),
    .O(Mux2xBit_inst35_O)
);
Mux2xBit Mux2xBit_inst36 (
    .I0(Register_inst0_O[36]),
    .I1(magma_Bits_8_lshr_inst36_out[0]),
    .S(magma_Bit_and_inst72_out),
    .O(Mux2xBit_inst36_O)
);
Mux2xBit Mux2xBit_inst37 (
    .I0(Register_inst0_O[37]),
    .I1(magma_Bits_8_lshr_inst37_out[0]),
    .S(magma_Bit_and_inst74_out),
    .O(Mux2xBit_inst37_O)
);
Mux2xBit Mux2xBit_inst38 (
    .I0(Register_inst0_O[38]),
    .I1(magma_Bits_8_lshr_inst38_out[0]),
    .S(magma_Bit_and_inst76_out),
    .O(Mux2xBit_inst38_O)
);
Mux2xBit Mux2xBit_inst39 (
    .I0(Register_inst0_O[39]),
    .I1(magma_Bits_8_lshr_inst39_out[0]),
    .S(magma_Bit_and_inst78_out),
    .O(Mux2xBit_inst39_O)
);
Mux2xBit Mux2xBit_inst4 (
    .I0(Register_inst0_O[4]),
    .I1(magma_Bits_8_lshr_inst4_out[0]),
    .S(magma_Bit_and_inst8_out),
    .O(Mux2xBit_inst4_O)
);
Mux2xBit Mux2xBit_inst40 (
    .I0(Register_inst0_O[40]),
    .I1(magma_Bits_8_lshr_inst40_out[0]),
    .S(magma_Bit_and_inst80_out),
    .O(Mux2xBit_inst40_O)
);
Mux2xBit Mux2xBit_inst41 (
    .I0(Register_inst0_O[41]),
    .I1(magma_Bits_8_lshr_inst41_out[0]),
    .S(magma_Bit_and_inst82_out),
    .O(Mux2xBit_inst41_O)
);
Mux2xBit Mux2xBit_inst42 (
    .I0(Register_inst0_O[42]),
    .I1(magma_Bits_8_lshr_inst42_out[0]),
    .S(magma_Bit_and_inst84_out),
    .O(Mux2xBit_inst42_O)
);
Mux2xBit Mux2xBit_inst43 (
    .I0(Register_inst0_O[43]),
    .I1(magma_Bits_8_lshr_inst43_out[0]),
    .S(magma_Bit_and_inst86_out),
    .O(Mux2xBit_inst43_O)
);
Mux2xBit Mux2xBit_inst44 (
    .I0(Register_inst0_O[44]),
    .I1(magma_Bits_8_lshr_inst44_out[0]),
    .S(magma_Bit_and_inst88_out),
    .O(Mux2xBit_inst44_O)
);
Mux2xBit Mux2xBit_inst45 (
    .I0(Register_inst0_O[45]),
    .I1(magma_Bits_8_lshr_inst45_out[0]),
    .S(magma_Bit_and_inst90_out),
    .O(Mux2xBit_inst45_O)
);
Mux2xBit Mux2xBit_inst46 (
    .I0(Register_inst0_O[46]),
    .I1(magma_Bits_8_lshr_inst46_out[0]),
    .S(magma_Bit_and_inst92_out),
    .O(Mux2xBit_inst46_O)
);
Mux2xBit Mux2xBit_inst47 (
    .I0(Register_inst0_O[47]),
    .I1(magma_Bits_8_lshr_inst47_out[0]),
    .S(magma_Bit_and_inst94_out),
    .O(Mux2xBit_inst47_O)
);
Mux2xBit Mux2xBit_inst48 (
    .I0(Register_inst0_O[48]),
    .I1(magma_Bits_8_lshr_inst48_out[0]),
    .S(magma_Bit_and_inst96_out),
    .O(Mux2xBit_inst48_O)
);
Mux2xBit Mux2xBit_inst49 (
    .I0(Register_inst0_O[49]),
    .I1(magma_Bits_8_lshr_inst49_out[0]),
    .S(magma_Bit_and_inst98_out),
    .O(Mux2xBit_inst49_O)
);
Mux2xBit Mux2xBit_inst5 (
    .I0(Register_inst0_O[5]),
    .I1(magma_Bits_8_lshr_inst5_out[0]),
    .S(magma_Bit_and_inst10_out),
    .O(Mux2xBit_inst5_O)
);
Mux2xBit Mux2xBit_inst50 (
    .I0(Register_inst0_O[50]),
    .I1(magma_Bits_8_lshr_inst50_out[0]),
    .S(magma_Bit_and_inst100_out),
    .O(Mux2xBit_inst50_O)
);
Mux2xBit Mux2xBit_inst51 (
    .I0(Register_inst0_O[51]),
    .I1(magma_Bits_8_lshr_inst51_out[0]),
    .S(magma_Bit_and_inst102_out),
    .O(Mux2xBit_inst51_O)
);
Mux2xBit Mux2xBit_inst52 (
    .I0(Register_inst0_O[52]),
    .I1(magma_Bits_8_lshr_inst52_out[0]),
    .S(magma_Bit_and_inst104_out),
    .O(Mux2xBit_inst52_O)
);
Mux2xBit Mux2xBit_inst53 (
    .I0(Register_inst0_O[53]),
    .I1(magma_Bits_8_lshr_inst53_out[0]),
    .S(magma_Bit_and_inst106_out),
    .O(Mux2xBit_inst53_O)
);
Mux2xBit Mux2xBit_inst54 (
    .I0(Register_inst0_O[54]),
    .I1(magma_Bits_8_lshr_inst54_out[0]),
    .S(magma_Bit_and_inst108_out),
    .O(Mux2xBit_inst54_O)
);
Mux2xBit Mux2xBit_inst55 (
    .I0(Register_inst0_O[55]),
    .I1(magma_Bits_8_lshr_inst55_out[0]),
    .S(magma_Bit_and_inst110_out),
    .O(Mux2xBit_inst55_O)
);
Mux2xBit Mux2xBit_inst56 (
    .I0(Register_inst0_O[56]),
    .I1(magma_Bits_8_lshr_inst56_out[0]),
    .S(magma_Bit_and_inst112_out),
    .O(Mux2xBit_inst56_O)
);
Mux2xBit Mux2xBit_inst57 (
    .I0(Register_inst0_O[57]),
    .I1(magma_Bits_8_lshr_inst57_out[0]),
    .S(magma_Bit_and_inst114_out),
    .O(Mux2xBit_inst57_O)
);
Mux2xBit Mux2xBit_inst58 (
    .I0(Register_inst0_O[58]),
    .I1(magma_Bits_8_lshr_inst58_out[0]),
    .S(magma_Bit_and_inst116_out),
    .O(Mux2xBit_inst58_O)
);
Mux2xBit Mux2xBit_inst59 (
    .I0(Register_inst0_O[59]),
    .I1(magma_Bits_8_lshr_inst59_out[0]),
    .S(magma_Bit_and_inst118_out),
    .O(Mux2xBit_inst59_O)
);
Mux2xBit Mux2xBit_inst6 (
    .I0(Register_inst0_O[6]),
    .I1(magma_Bits_8_lshr_inst6_out[0]),
    .S(magma_Bit_and_inst12_out),
    .O(Mux2xBit_inst6_O)
);
Mux2xBit Mux2xBit_inst60 (
    .I0(Register_inst0_O[60]),
    .I1(magma_Bits_8_lshr_inst60_out[0]),
    .S(magma_Bit_and_inst120_out),
    .O(Mux2xBit_inst60_O)
);
Mux2xBit Mux2xBit_inst61 (
    .I0(Register_inst0_O[61]),
    .I1(magma_Bits_8_lshr_inst61_out[0]),
    .S(magma_Bit_and_inst122_out),
    .O(Mux2xBit_inst61_O)
);
Mux2xBit Mux2xBit_inst62 (
    .I0(Register_inst0_O[62]),
    .I1(magma_Bits_8_lshr_inst62_out[0]),
    .S(magma_Bit_and_inst124_out),
    .O(Mux2xBit_inst62_O)
);
Mux2xBit Mux2xBit_inst63 (
    .I0(Register_inst0_O[63]),
    .I1(magma_Bits_8_lshr_inst63_out[0]),
    .S(magma_Bit_and_inst125_out),
    .O(Mux2xBit_inst63_O)
);
Mux2xBit Mux2xBit_inst7 (
    .I0(Register_inst0_O[7]),
    .I1(magma_Bits_8_lshr_inst7_out[0]),
    .S(magma_Bit_and_inst14_out),
    .O(Mux2xBit_inst7_O)
);
Mux2xBit Mux2xBit_inst8 (
    .I0(Register_inst0_O[8]),
    .I1(magma_Bits_8_lshr_inst8_out[0]),
    .S(magma_Bit_and_inst16_out),
    .O(Mux2xBit_inst8_O)
);
Mux2xBit Mux2xBit_inst9 (
    .I0(Register_inst0_O[9]),
    .I1(magma_Bits_8_lshr_inst9_out[0]),
    .S(magma_Bit_and_inst18_out),
    .O(Mux2xBit_inst9_O)
);
wire [7:0] Mux56xBits8_inst0_I0;
assign Mux56xBits8_inst0_I0 = {Register_inst0_O[7],Register_inst0_O[6],Register_inst0_O[5],Register_inst0_O[4],Register_inst0_O[3],Register_inst0_O[2],Register_inst0_O[1],Register_inst0_O[0]};
wire [7:0] Mux56xBits8_inst0_I1;
assign Mux56xBits8_inst0_I1 = {Register_inst0_O[8],Register_inst0_O[7],Register_inst0_O[6],Register_inst0_O[5],Register_inst0_O[4],Register_inst0_O[3],Register_inst0_O[2],Register_inst0_O[1]};
wire [7:0] Mux56xBits8_inst0_I2;
assign Mux56xBits8_inst0_I2 = {Register_inst0_O[9],Register_inst0_O[8],Register_inst0_O[7],Register_inst0_O[6],Register_inst0_O[5],Register_inst0_O[4],Register_inst0_O[3],Register_inst0_O[2]};
wire [7:0] Mux56xBits8_inst0_I3;
assign Mux56xBits8_inst0_I3 = {Register_inst0_O[10],Register_inst0_O[9],Register_inst0_O[8],Register_inst0_O[7],Register_inst0_O[6],Register_inst0_O[5],Register_inst0_O[4],Register_inst0_O[3]};
wire [7:0] Mux56xBits8_inst0_I4;
assign Mux56xBits8_inst0_I4 = {Register_inst0_O[11],Register_inst0_O[10],Register_inst0_O[9],Register_inst0_O[8],Register_inst0_O[7],Register_inst0_O[6],Register_inst0_O[5],Register_inst0_O[4]};
wire [7:0] Mux56xBits8_inst0_I5;
assign Mux56xBits8_inst0_I5 = {Register_inst0_O[12],Register_inst0_O[11],Register_inst0_O[10],Register_inst0_O[9],Register_inst0_O[8],Register_inst0_O[7],Register_inst0_O[6],Register_inst0_O[5]};
wire [7:0] Mux56xBits8_inst0_I6;
assign Mux56xBits8_inst0_I6 = {Register_inst0_O[13],Register_inst0_O[12],Register_inst0_O[11],Register_inst0_O[10],Register_inst0_O[9],Register_inst0_O[8],Register_inst0_O[7],Register_inst0_O[6]};
wire [7:0] Mux56xBits8_inst0_I7;
assign Mux56xBits8_inst0_I7 = {Register_inst0_O[14],Register_inst0_O[13],Register_inst0_O[12],Register_inst0_O[11],Register_inst0_O[10],Register_inst0_O[9],Register_inst0_O[8],Register_inst0_O[7]};
wire [7:0] Mux56xBits8_inst0_I8;
assign Mux56xBits8_inst0_I8 = {Register_inst0_O[15],Register_inst0_O[14],Register_inst0_O[13],Register_inst0_O[12],Register_inst0_O[11],Register_inst0_O[10],Register_inst0_O[9],Register_inst0_O[8]};
wire [7:0] Mux56xBits8_inst0_I9;
assign Mux56xBits8_inst0_I9 = {Register_inst0_O[16],Register_inst0_O[15],Register_inst0_O[14],Register_inst0_O[13],Register_inst0_O[12],Register_inst0_O[11],Register_inst0_O[10],Register_inst0_O[9]};
wire [7:0] Mux56xBits8_inst0_I10;
assign Mux56xBits8_inst0_I10 = {Register_inst0_O[17],Register_inst0_O[16],Register_inst0_O[15],Register_inst0_O[14],Register_inst0_O[13],Register_inst0_O[12],Register_inst0_O[11],Register_inst0_O[10]};
wire [7:0] Mux56xBits8_inst0_I11;
assign Mux56xBits8_inst0_I11 = {Register_inst0_O[18],Register_inst0_O[17],Register_inst0_O[16],Register_inst0_O[15],Register_inst0_O[14],Register_inst0_O[13],Register_inst0_O[12],Register_inst0_O[11]};
wire [7:0] Mux56xBits8_inst0_I12;
assign Mux56xBits8_inst0_I12 = {Register_inst0_O[19],Register_inst0_O[18],Register_inst0_O[17],Register_inst0_O[16],Register_inst0_O[15],Register_inst0_O[14],Register_inst0_O[13],Register_inst0_O[12]};
wire [7:0] Mux56xBits8_inst0_I13;
assign Mux56xBits8_inst0_I13 = {Register_inst0_O[20],Register_inst0_O[19],Register_inst0_O[18],Register_inst0_O[17],Register_inst0_O[16],Register_inst0_O[15],Register_inst0_O[14],Register_inst0_O[13]};
wire [7:0] Mux56xBits8_inst0_I14;
assign Mux56xBits8_inst0_I14 = {Register_inst0_O[21],Register_inst0_O[20],Register_inst0_O[19],Register_inst0_O[18],Register_inst0_O[17],Register_inst0_O[16],Register_inst0_O[15],Register_inst0_O[14]};
wire [7:0] Mux56xBits8_inst0_I15;
assign Mux56xBits8_inst0_I15 = {Register_inst0_O[22],Register_inst0_O[21],Register_inst0_O[20],Register_inst0_O[19],Register_inst0_O[18],Register_inst0_O[17],Register_inst0_O[16],Register_inst0_O[15]};
wire [7:0] Mux56xBits8_inst0_I16;
assign Mux56xBits8_inst0_I16 = {Register_inst0_O[23],Register_inst0_O[22],Register_inst0_O[21],Register_inst0_O[20],Register_inst0_O[19],Register_inst0_O[18],Register_inst0_O[17],Register_inst0_O[16]};
wire [7:0] Mux56xBits8_inst0_I17;
assign Mux56xBits8_inst0_I17 = {Register_inst0_O[24],Register_inst0_O[23],Register_inst0_O[22],Register_inst0_O[21],Register_inst0_O[20],Register_inst0_O[19],Register_inst0_O[18],Register_inst0_O[17]};
wire [7:0] Mux56xBits8_inst0_I18;
assign Mux56xBits8_inst0_I18 = {Register_inst0_O[25],Register_inst0_O[24],Register_inst0_O[23],Register_inst0_O[22],Register_inst0_O[21],Register_inst0_O[20],Register_inst0_O[19],Register_inst0_O[18]};
wire [7:0] Mux56xBits8_inst0_I19;
assign Mux56xBits8_inst0_I19 = {Register_inst0_O[26],Register_inst0_O[25],Register_inst0_O[24],Register_inst0_O[23],Register_inst0_O[22],Register_inst0_O[21],Register_inst0_O[20],Register_inst0_O[19]};
wire [7:0] Mux56xBits8_inst0_I20;
assign Mux56xBits8_inst0_I20 = {Register_inst0_O[27],Register_inst0_O[26],Register_inst0_O[25],Register_inst0_O[24],Register_inst0_O[23],Register_inst0_O[22],Register_inst0_O[21],Register_inst0_O[20]};
wire [7:0] Mux56xBits8_inst0_I21;
assign Mux56xBits8_inst0_I21 = {Register_inst0_O[28],Register_inst0_O[27],Register_inst0_O[26],Register_inst0_O[25],Register_inst0_O[24],Register_inst0_O[23],Register_inst0_O[22],Register_inst0_O[21]};
wire [7:0] Mux56xBits8_inst0_I22;
assign Mux56xBits8_inst0_I22 = {Register_inst0_O[29],Register_inst0_O[28],Register_inst0_O[27],Register_inst0_O[26],Register_inst0_O[25],Register_inst0_O[24],Register_inst0_O[23],Register_inst0_O[22]};
wire [7:0] Mux56xBits8_inst0_I23;
assign Mux56xBits8_inst0_I23 = {Register_inst0_O[30],Register_inst0_O[29],Register_inst0_O[28],Register_inst0_O[27],Register_inst0_O[26],Register_inst0_O[25],Register_inst0_O[24],Register_inst0_O[23]};
wire [7:0] Mux56xBits8_inst0_I24;
assign Mux56xBits8_inst0_I24 = {Register_inst0_O[31],Register_inst0_O[30],Register_inst0_O[29],Register_inst0_O[28],Register_inst0_O[27],Register_inst0_O[26],Register_inst0_O[25],Register_inst0_O[24]};
wire [7:0] Mux56xBits8_inst0_I25;
assign Mux56xBits8_inst0_I25 = {Register_inst0_O[32],Register_inst0_O[31],Register_inst0_O[30],Register_inst0_O[29],Register_inst0_O[28],Register_inst0_O[27],Register_inst0_O[26],Register_inst0_O[25]};
wire [7:0] Mux56xBits8_inst0_I26;
assign Mux56xBits8_inst0_I26 = {Register_inst0_O[33],Register_inst0_O[32],Register_inst0_O[31],Register_inst0_O[30],Register_inst0_O[29],Register_inst0_O[28],Register_inst0_O[27],Register_inst0_O[26]};
wire [7:0] Mux56xBits8_inst0_I27;
assign Mux56xBits8_inst0_I27 = {Register_inst0_O[34],Register_inst0_O[33],Register_inst0_O[32],Register_inst0_O[31],Register_inst0_O[30],Register_inst0_O[29],Register_inst0_O[28],Register_inst0_O[27]};
wire [7:0] Mux56xBits8_inst0_I28;
assign Mux56xBits8_inst0_I28 = {Register_inst0_O[35],Register_inst0_O[34],Register_inst0_O[33],Register_inst0_O[32],Register_inst0_O[31],Register_inst0_O[30],Register_inst0_O[29],Register_inst0_O[28]};
wire [7:0] Mux56xBits8_inst0_I29;
assign Mux56xBits8_inst0_I29 = {Register_inst0_O[36],Register_inst0_O[35],Register_inst0_O[34],Register_inst0_O[33],Register_inst0_O[32],Register_inst0_O[31],Register_inst0_O[30],Register_inst0_O[29]};
wire [7:0] Mux56xBits8_inst0_I30;
assign Mux56xBits8_inst0_I30 = {Register_inst0_O[37],Register_inst0_O[36],Register_inst0_O[35],Register_inst0_O[34],Register_inst0_O[33],Register_inst0_O[32],Register_inst0_O[31],Register_inst0_O[30]};
wire [7:0] Mux56xBits8_inst0_I31;
assign Mux56xBits8_inst0_I31 = {Register_inst0_O[38],Register_inst0_O[37],Register_inst0_O[36],Register_inst0_O[35],Register_inst0_O[34],Register_inst0_O[33],Register_inst0_O[32],Register_inst0_O[31]};
wire [7:0] Mux56xBits8_inst0_I32;
assign Mux56xBits8_inst0_I32 = {Register_inst0_O[39],Register_inst0_O[38],Register_inst0_O[37],Register_inst0_O[36],Register_inst0_O[35],Register_inst0_O[34],Register_inst0_O[33],Register_inst0_O[32]};
wire [7:0] Mux56xBits8_inst0_I33;
assign Mux56xBits8_inst0_I33 = {Register_inst0_O[40],Register_inst0_O[39],Register_inst0_O[38],Register_inst0_O[37],Register_inst0_O[36],Register_inst0_O[35],Register_inst0_O[34],Register_inst0_O[33]};
wire [7:0] Mux56xBits8_inst0_I34;
assign Mux56xBits8_inst0_I34 = {Register_inst0_O[41],Register_inst0_O[40],Register_inst0_O[39],Register_inst0_O[38],Register_inst0_O[37],Register_inst0_O[36],Register_inst0_O[35],Register_inst0_O[34]};
wire [7:0] Mux56xBits8_inst0_I35;
assign Mux56xBits8_inst0_I35 = {Register_inst0_O[42],Register_inst0_O[41],Register_inst0_O[40],Register_inst0_O[39],Register_inst0_O[38],Register_inst0_O[37],Register_inst0_O[36],Register_inst0_O[35]};
wire [7:0] Mux56xBits8_inst0_I36;
assign Mux56xBits8_inst0_I36 = {Register_inst0_O[43],Register_inst0_O[42],Register_inst0_O[41],Register_inst0_O[40],Register_inst0_O[39],Register_inst0_O[38],Register_inst0_O[37],Register_inst0_O[36]};
wire [7:0] Mux56xBits8_inst0_I37;
assign Mux56xBits8_inst0_I37 = {Register_inst0_O[44],Register_inst0_O[43],Register_inst0_O[42],Register_inst0_O[41],Register_inst0_O[40],Register_inst0_O[39],Register_inst0_O[38],Register_inst0_O[37]};
wire [7:0] Mux56xBits8_inst0_I38;
assign Mux56xBits8_inst0_I38 = {Register_inst0_O[45],Register_inst0_O[44],Register_inst0_O[43],Register_inst0_O[42],Register_inst0_O[41],Register_inst0_O[40],Register_inst0_O[39],Register_inst0_O[38]};
wire [7:0] Mux56xBits8_inst0_I39;
assign Mux56xBits8_inst0_I39 = {Register_inst0_O[46],Register_inst0_O[45],Register_inst0_O[44],Register_inst0_O[43],Register_inst0_O[42],Register_inst0_O[41],Register_inst0_O[40],Register_inst0_O[39]};
wire [7:0] Mux56xBits8_inst0_I40;
assign Mux56xBits8_inst0_I40 = {Register_inst0_O[47],Register_inst0_O[46],Register_inst0_O[45],Register_inst0_O[44],Register_inst0_O[43],Register_inst0_O[42],Register_inst0_O[41],Register_inst0_O[40]};
wire [7:0] Mux56xBits8_inst0_I41;
assign Mux56xBits8_inst0_I41 = {Register_inst0_O[48],Register_inst0_O[47],Register_inst0_O[46],Register_inst0_O[45],Register_inst0_O[44],Register_inst0_O[43],Register_inst0_O[42],Register_inst0_O[41]};
wire [7:0] Mux56xBits8_inst0_I42;
assign Mux56xBits8_inst0_I42 = {Register_inst0_O[49],Register_inst0_O[48],Register_inst0_O[47],Register_inst0_O[46],Register_inst0_O[45],Register_inst0_O[44],Register_inst0_O[43],Register_inst0_O[42]};
wire [7:0] Mux56xBits8_inst0_I43;
assign Mux56xBits8_inst0_I43 = {Register_inst0_O[50],Register_inst0_O[49],Register_inst0_O[48],Register_inst0_O[47],Register_inst0_O[46],Register_inst0_O[45],Register_inst0_O[44],Register_inst0_O[43]};
wire [7:0] Mux56xBits8_inst0_I44;
assign Mux56xBits8_inst0_I44 = {Register_inst0_O[51],Register_inst0_O[50],Register_inst0_O[49],Register_inst0_O[48],Register_inst0_O[47],Register_inst0_O[46],Register_inst0_O[45],Register_inst0_O[44]};
wire [7:0] Mux56xBits8_inst0_I45;
assign Mux56xBits8_inst0_I45 = {Register_inst0_O[52],Register_inst0_O[51],Register_inst0_O[50],Register_inst0_O[49],Register_inst0_O[48],Register_inst0_O[47],Register_inst0_O[46],Register_inst0_O[45]};
wire [7:0] Mux56xBits8_inst0_I46;
assign Mux56xBits8_inst0_I46 = {Register_inst0_O[53],Register_inst0_O[52],Register_inst0_O[51],Register_inst0_O[50],Register_inst0_O[49],Register_inst0_O[48],Register_inst0_O[47],Register_inst0_O[46]};
wire [7:0] Mux56xBits8_inst0_I47;
assign Mux56xBits8_inst0_I47 = {Register_inst0_O[54],Register_inst0_O[53],Register_inst0_O[52],Register_inst0_O[51],Register_inst0_O[50],Register_inst0_O[49],Register_inst0_O[48],Register_inst0_O[47]};
wire [7:0] Mux56xBits8_inst0_I48;
assign Mux56xBits8_inst0_I48 = {Register_inst0_O[55],Register_inst0_O[54],Register_inst0_O[53],Register_inst0_O[52],Register_inst0_O[51],Register_inst0_O[50],Register_inst0_O[49],Register_inst0_O[48]};
wire [7:0] Mux56xBits8_inst0_I49;
assign Mux56xBits8_inst0_I49 = {Register_inst0_O[56],Register_inst0_O[55],Register_inst0_O[54],Register_inst0_O[53],Register_inst0_O[52],Register_inst0_O[51],Register_inst0_O[50],Register_inst0_O[49]};
wire [7:0] Mux56xBits8_inst0_I50;
assign Mux56xBits8_inst0_I50 = {Register_inst0_O[57],Register_inst0_O[56],Register_inst0_O[55],Register_inst0_O[54],Register_inst0_O[53],Register_inst0_O[52],Register_inst0_O[51],Register_inst0_O[50]};
wire [7:0] Mux56xBits8_inst0_I51;
assign Mux56xBits8_inst0_I51 = {Register_inst0_O[58],Register_inst0_O[57],Register_inst0_O[56],Register_inst0_O[55],Register_inst0_O[54],Register_inst0_O[53],Register_inst0_O[52],Register_inst0_O[51]};
wire [7:0] Mux56xBits8_inst0_I52;
assign Mux56xBits8_inst0_I52 = {Register_inst0_O[59],Register_inst0_O[58],Register_inst0_O[57],Register_inst0_O[56],Register_inst0_O[55],Register_inst0_O[54],Register_inst0_O[53],Register_inst0_O[52]};
wire [7:0] Mux56xBits8_inst0_I53;
assign Mux56xBits8_inst0_I53 = {Register_inst0_O[60],Register_inst0_O[59],Register_inst0_O[58],Register_inst0_O[57],Register_inst0_O[56],Register_inst0_O[55],Register_inst0_O[54],Register_inst0_O[53]};
wire [7:0] Mux56xBits8_inst0_I54;
assign Mux56xBits8_inst0_I54 = {Register_inst0_O[61],Register_inst0_O[60],Register_inst0_O[59],Register_inst0_O[58],Register_inst0_O[57],Register_inst0_O[56],Register_inst0_O[55],Register_inst0_O[54]};
wire [7:0] Mux56xBits8_inst0_I55;
assign Mux56xBits8_inst0_I55 = {Register_inst0_O[62],Register_inst0_O[61],Register_inst0_O[60],Register_inst0_O[59],Register_inst0_O[58],Register_inst0_O[57],Register_inst0_O[56],Register_inst0_O[55]};
Mux56xBits8 Mux56xBits8_inst0 (
    .I0(Mux56xBits8_inst0_I0),
    .I1(Mux56xBits8_inst0_I1),
    .I2(Mux56xBits8_inst0_I2),
    .I3(Mux56xBits8_inst0_I3),
    .I4(Mux56xBits8_inst0_I4),
    .I5(Mux56xBits8_inst0_I5),
    .I6(Mux56xBits8_inst0_I6),
    .I7(Mux56xBits8_inst0_I7),
    .I8(Mux56xBits8_inst0_I8),
    .I9(Mux56xBits8_inst0_I9),
    .I10(Mux56xBits8_inst0_I10),
    .I11(Mux56xBits8_inst0_I11),
    .I12(Mux56xBits8_inst0_I12),
    .I13(Mux56xBits8_inst0_I13),
    .I14(Mux56xBits8_inst0_I14),
    .I15(Mux56xBits8_inst0_I15),
    .I16(Mux56xBits8_inst0_I16),
    .I17(Mux56xBits8_inst0_I17),
    .I18(Mux56xBits8_inst0_I18),
    .I19(Mux56xBits8_inst0_I19),
    .I20(Mux56xBits8_inst0_I20),
    .I21(Mux56xBits8_inst0_I21),
    .I22(Mux56xBits8_inst0_I22),
    .I23(Mux56xBits8_inst0_I23),
    .I24(Mux56xBits8_inst0_I24),
    .I25(Mux56xBits8_inst0_I25),
    .I26(Mux56xBits8_inst0_I26),
    .I27(Mux56xBits8_inst0_I27),
    .I28(Mux56xBits8_inst0_I28),
    .I29(Mux56xBits8_inst0_I29),
    .I30(Mux56xBits8_inst0_I30),
    .I31(Mux56xBits8_inst0_I31),
    .I32(Mux56xBits8_inst0_I32),
    .I33(Mux56xBits8_inst0_I33),
    .I34(Mux56xBits8_inst0_I34),
    .I35(Mux56xBits8_inst0_I35),
    .I36(Mux56xBits8_inst0_I36),
    .I37(Mux56xBits8_inst0_I37),
    .I38(Mux56xBits8_inst0_I38),
    .I39(Mux56xBits8_inst0_I39),
    .I40(Mux56xBits8_inst0_I40),
    .I41(Mux56xBits8_inst0_I41),
    .I42(Mux56xBits8_inst0_I42),
    .I43(Mux56xBits8_inst0_I43),
    .I44(Mux56xBits8_inst0_I44),
    .I45(Mux56xBits8_inst0_I45),
    .I46(Mux56xBits8_inst0_I46),
    .I47(Mux56xBits8_inst0_I47),
    .I48(Mux56xBits8_inst0_I48),
    .I49(Mux56xBits8_inst0_I49),
    .I50(Mux56xBits8_inst0_I50),
    .I51(Mux56xBits8_inst0_I51),
    .I52(Mux56xBits8_inst0_I52),
    .I53(Mux56xBits8_inst0_I53),
    .I54(Mux56xBits8_inst0_I54),
    .I55(Mux56xBits8_inst0_I55),
    .S(magma_UInt_6_mul_inst0_out),
    .O(O)
);
wire [63:0] Register_inst0_I;
assign Register_inst0_I = {Mux2xBit_inst63_O,Mux2xBit_inst62_O,Mux2xBit_inst61_O,Mux2xBit_inst60_O,Mux2xBit_inst59_O,Mux2xBit_inst58_O,Mux2xBit_inst57_O,Mux2xBit_inst56_O,Mux2xBit_inst55_O,Mux2xBit_inst54_O,Mux2xBit_inst53_O,Mux2xBit_inst52_O,Mux2xBit_inst51_O,Mux2xBit_inst50_O,Mux2xBit_inst49_O,Mux2xBit_inst48_O,Mux2xBit_inst47_O,Mux2xBit_inst46_O,Mux2xBit_inst45_O,Mux2xBit_inst44_O,Mux2xBit_inst43_O,Mux2xBit_inst42_O,Mux2xBit_inst41_O,Mux2xBit_inst40_O,Mux2xBit_inst39_O,Mux2xBit_inst38_O,Mux2xBit_inst37_O,Mux2xBit_inst36_O,Mux2xBit_inst35_O,Mux2xBit_inst34_O,Mux2xBit_inst33_O,Mux2xBit_inst32_O,Mux2xBit_inst31_O,Mux2xBit_inst30_O,Mux2xBit_inst29_O,Mux2xBit_inst28_O,Mux2xBit_inst27_O,Mux2xBit_inst26_O,Mux2xBit_inst25_O,Mux2xBit_inst24_O,Mux2xBit_inst23_O,Mux2xBit_inst22_O,Mux2xBit_inst21_O,Mux2xBit_inst20_O,Mux2xBit_inst19_O,Mux2xBit_inst18_O,Mux2xBit_inst17_O,Mux2xBit_inst16_O,Mux2xBit_inst15_O,Mux2xBit_inst14_O,Mux2xBit_inst13_O,Mux2xBit_inst12_O,Mux2xBit_inst11_O,Mux2xBit_inst10_O,Mux2xBit_inst9_O,Mux2xBit_inst8_O,Mux2xBit_inst7_O,Mux2xBit_inst6_O,Mux2xBit_inst5_O,Mux2xBit_inst4_O,Mux2xBit_inst3_O,Mux2xBit_inst2_O,Mux2xBit_inst1_O,Mux2xBit_inst0_O};
Register Register_inst0 (
    .I(Register_inst0_I),
    .O(Register_inst0_O),
    .CLK(CLK)
);
assign magma_Bit_and_inst0_out = 1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h00);
assign magma_Bit_and_inst10_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h05)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h05);
assign magma_Bit_and_inst100_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h32)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h32);
assign magma_Bit_and_inst102_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h33)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h33);
assign magma_Bit_and_inst104_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h34)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h34);
assign magma_Bit_and_inst106_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h35)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h35);
assign magma_Bit_and_inst108_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h36)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h36);
assign magma_Bit_and_inst110_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h37)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h37);
assign magma_Bit_and_inst112_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h38)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h38);
assign magma_Bit_and_inst114_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h39)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h39);
assign magma_Bit_and_inst116_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h3a)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3a);
assign magma_Bit_and_inst118_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h3b)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3b);
assign magma_Bit_and_inst12_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h06)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h06);
assign magma_Bit_and_inst120_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h3c)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3c);
assign magma_Bit_and_inst122_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h3d)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3d);
assign magma_Bit_and_inst124_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h3e)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3e);
assign magma_Bit_and_inst125_out = 1'b1 & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h3f);
assign magma_Bit_and_inst14_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h07)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h07);
assign magma_Bit_and_inst16_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h08)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h08);
assign magma_Bit_and_inst18_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h09)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h09);
assign magma_Bit_and_inst2_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h01)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h01);
assign magma_Bit_and_inst20_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h0a)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0a);
assign magma_Bit_and_inst22_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h0b)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0b);
assign magma_Bit_and_inst24_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h0c)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0c);
assign magma_Bit_and_inst26_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h0d)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0d);
assign magma_Bit_and_inst28_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h0e)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0e);
assign magma_Bit_and_inst30_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h0f)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h0f);
assign magma_Bit_and_inst32_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h10)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h10);
assign magma_Bit_and_inst34_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h11)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h11);
assign magma_Bit_and_inst36_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h12)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h12);
assign magma_Bit_and_inst38_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h13)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h13);
assign magma_Bit_and_inst4_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h02)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h02);
assign magma_Bit_and_inst40_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h14)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h14);
assign magma_Bit_and_inst42_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h15)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h15);
assign magma_Bit_and_inst44_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h16)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h16);
assign magma_Bit_and_inst46_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h17)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h17);
assign magma_Bit_and_inst48_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h18)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h18);
assign magma_Bit_and_inst50_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h19)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h19);
assign magma_Bit_and_inst52_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h1a)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1a);
assign magma_Bit_and_inst54_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h1b)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1b);
assign magma_Bit_and_inst56_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h1c)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1c);
assign magma_Bit_and_inst58_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h1d)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1d);
assign magma_Bit_and_inst6_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h03)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h03);
assign magma_Bit_and_inst60_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h1e)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1e);
assign magma_Bit_and_inst62_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h1f)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h1f);
assign magma_Bit_and_inst64_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h20)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h20);
assign magma_Bit_and_inst66_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h21)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h21);
assign magma_Bit_and_inst68_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h22)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h22);
assign magma_Bit_and_inst70_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h23)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h23);
assign magma_Bit_and_inst72_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h24)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h24);
assign magma_Bit_and_inst74_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h25)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h25);
assign magma_Bit_and_inst76_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h26)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h26);
assign magma_Bit_and_inst78_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h27)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h27);
assign magma_Bit_and_inst8_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h04)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h04);
assign magma_Bit_and_inst80_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h28)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h28);
assign magma_Bit_and_inst82_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h29)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h29);
assign magma_Bit_and_inst84_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h2a)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2a);
assign magma_Bit_and_inst86_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h2b)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2b);
assign magma_Bit_and_inst88_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h2c)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2c);
assign magma_Bit_and_inst90_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h2d)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2d);
assign magma_Bit_and_inst92_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h2e)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2e);
assign magma_Bit_and_inst94_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h2f)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h2f);
assign magma_Bit_and_inst96_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h30)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h30);
assign magma_Bit_and_inst98_out = (1'b1 & (magma_UInt_6_mul_inst1_out <= 6'h31)) & ((6'((6'(magma_UInt_6_mul_inst1_out + 6'h08)) - 6'h01)) >= 6'h31);
assign magma_Bits_8_lshr_inst0_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst0_out[2],magma_UInt_6_sub_inst0_out[1],magma_UInt_6_sub_inst0_out[0]});
assign magma_Bits_8_lshr_inst1_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst2_out[2],magma_UInt_6_sub_inst2_out[1],magma_UInt_6_sub_inst2_out[0]});
assign magma_Bits_8_lshr_inst10_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst20_out[2],magma_UInt_6_sub_inst20_out[1],magma_UInt_6_sub_inst20_out[0]});
assign magma_Bits_8_lshr_inst11_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst22_out[2],magma_UInt_6_sub_inst22_out[1],magma_UInt_6_sub_inst22_out[0]});
assign magma_Bits_8_lshr_inst12_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst24_out[2],magma_UInt_6_sub_inst24_out[1],magma_UInt_6_sub_inst24_out[0]});
assign magma_Bits_8_lshr_inst13_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst26_out[2],magma_UInt_6_sub_inst26_out[1],magma_UInt_6_sub_inst26_out[0]});
assign magma_Bits_8_lshr_inst14_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst28_out[2],magma_UInt_6_sub_inst28_out[1],magma_UInt_6_sub_inst28_out[0]});
assign magma_Bits_8_lshr_inst15_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst30_out[2],magma_UInt_6_sub_inst30_out[1],magma_UInt_6_sub_inst30_out[0]});
assign magma_Bits_8_lshr_inst16_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst32_out[2],magma_UInt_6_sub_inst32_out[1],magma_UInt_6_sub_inst32_out[0]});
assign magma_Bits_8_lshr_inst17_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst34_out[2],magma_UInt_6_sub_inst34_out[1],magma_UInt_6_sub_inst34_out[0]});
assign magma_Bits_8_lshr_inst18_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst36_out[2],magma_UInt_6_sub_inst36_out[1],magma_UInt_6_sub_inst36_out[0]});
assign magma_Bits_8_lshr_inst19_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst38_out[2],magma_UInt_6_sub_inst38_out[1],magma_UInt_6_sub_inst38_out[0]});
assign magma_Bits_8_lshr_inst2_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst4_out[2],magma_UInt_6_sub_inst4_out[1],magma_UInt_6_sub_inst4_out[0]});
assign magma_Bits_8_lshr_inst20_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst40_out[2],magma_UInt_6_sub_inst40_out[1],magma_UInt_6_sub_inst40_out[0]});
assign magma_Bits_8_lshr_inst21_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst42_out[2],magma_UInt_6_sub_inst42_out[1],magma_UInt_6_sub_inst42_out[0]});
assign magma_Bits_8_lshr_inst22_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst44_out[2],magma_UInt_6_sub_inst44_out[1],magma_UInt_6_sub_inst44_out[0]});
assign magma_Bits_8_lshr_inst23_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst46_out[2],magma_UInt_6_sub_inst46_out[1],magma_UInt_6_sub_inst46_out[0]});
assign magma_Bits_8_lshr_inst24_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst48_out[2],magma_UInt_6_sub_inst48_out[1],magma_UInt_6_sub_inst48_out[0]});
assign magma_Bits_8_lshr_inst25_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst50_out[2],magma_UInt_6_sub_inst50_out[1],magma_UInt_6_sub_inst50_out[0]});
assign magma_Bits_8_lshr_inst26_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst52_out[2],magma_UInt_6_sub_inst52_out[1],magma_UInt_6_sub_inst52_out[0]});
assign magma_Bits_8_lshr_inst27_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst54_out[2],magma_UInt_6_sub_inst54_out[1],magma_UInt_6_sub_inst54_out[0]});
assign magma_Bits_8_lshr_inst28_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst56_out[2],magma_UInt_6_sub_inst56_out[1],magma_UInt_6_sub_inst56_out[0]});
assign magma_Bits_8_lshr_inst29_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst58_out[2],magma_UInt_6_sub_inst58_out[1],magma_UInt_6_sub_inst58_out[0]});
assign magma_Bits_8_lshr_inst3_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst6_out[2],magma_UInt_6_sub_inst6_out[1],magma_UInt_6_sub_inst6_out[0]});
assign magma_Bits_8_lshr_inst30_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst60_out[2],magma_UInt_6_sub_inst60_out[1],magma_UInt_6_sub_inst60_out[0]});
assign magma_Bits_8_lshr_inst31_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst62_out[2],magma_UInt_6_sub_inst62_out[1],magma_UInt_6_sub_inst62_out[0]});
assign magma_Bits_8_lshr_inst32_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst64_out[2],magma_UInt_6_sub_inst64_out[1],magma_UInt_6_sub_inst64_out[0]});
assign magma_Bits_8_lshr_inst33_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst66_out[2],magma_UInt_6_sub_inst66_out[1],magma_UInt_6_sub_inst66_out[0]});
assign magma_Bits_8_lshr_inst34_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst68_out[2],magma_UInt_6_sub_inst68_out[1],magma_UInt_6_sub_inst68_out[0]});
assign magma_Bits_8_lshr_inst35_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst70_out[2],magma_UInt_6_sub_inst70_out[1],magma_UInt_6_sub_inst70_out[0]});
assign magma_Bits_8_lshr_inst36_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst72_out[2],magma_UInt_6_sub_inst72_out[1],magma_UInt_6_sub_inst72_out[0]});
assign magma_Bits_8_lshr_inst37_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst74_out[2],magma_UInt_6_sub_inst74_out[1],magma_UInt_6_sub_inst74_out[0]});
assign magma_Bits_8_lshr_inst38_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst76_out[2],magma_UInt_6_sub_inst76_out[1],magma_UInt_6_sub_inst76_out[0]});
assign magma_Bits_8_lshr_inst39_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst78_out[2],magma_UInt_6_sub_inst78_out[1],magma_UInt_6_sub_inst78_out[0]});
assign magma_Bits_8_lshr_inst4_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst8_out[2],magma_UInt_6_sub_inst8_out[1],magma_UInt_6_sub_inst8_out[0]});
assign magma_Bits_8_lshr_inst40_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst80_out[2],magma_UInt_6_sub_inst80_out[1],magma_UInt_6_sub_inst80_out[0]});
assign magma_Bits_8_lshr_inst41_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst82_out[2],magma_UInt_6_sub_inst82_out[1],magma_UInt_6_sub_inst82_out[0]});
assign magma_Bits_8_lshr_inst42_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst84_out[2],magma_UInt_6_sub_inst84_out[1],magma_UInt_6_sub_inst84_out[0]});
assign magma_Bits_8_lshr_inst43_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst86_out[2],magma_UInt_6_sub_inst86_out[1],magma_UInt_6_sub_inst86_out[0]});
assign magma_Bits_8_lshr_inst44_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst88_out[2],magma_UInt_6_sub_inst88_out[1],magma_UInt_6_sub_inst88_out[0]});
assign magma_Bits_8_lshr_inst45_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst90_out[2],magma_UInt_6_sub_inst90_out[1],magma_UInt_6_sub_inst90_out[0]});
assign magma_Bits_8_lshr_inst46_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst92_out[2],magma_UInt_6_sub_inst92_out[1],magma_UInt_6_sub_inst92_out[0]});
assign magma_Bits_8_lshr_inst47_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst94_out[2],magma_UInt_6_sub_inst94_out[1],magma_UInt_6_sub_inst94_out[0]});
assign magma_Bits_8_lshr_inst48_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst96_out[2],magma_UInt_6_sub_inst96_out[1],magma_UInt_6_sub_inst96_out[0]});
assign magma_Bits_8_lshr_inst49_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst98_out[2],magma_UInt_6_sub_inst98_out[1],magma_UInt_6_sub_inst98_out[0]});
assign magma_Bits_8_lshr_inst5_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst10_out[2],magma_UInt_6_sub_inst10_out[1],magma_UInt_6_sub_inst10_out[0]});
assign magma_Bits_8_lshr_inst50_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst100_out[2],magma_UInt_6_sub_inst100_out[1],magma_UInt_6_sub_inst100_out[0]});
assign magma_Bits_8_lshr_inst51_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst102_out[2],magma_UInt_6_sub_inst102_out[1],magma_UInt_6_sub_inst102_out[0]});
assign magma_Bits_8_lshr_inst52_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst104_out[2],magma_UInt_6_sub_inst104_out[1],magma_UInt_6_sub_inst104_out[0]});
assign magma_Bits_8_lshr_inst53_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst106_out[2],magma_UInt_6_sub_inst106_out[1],magma_UInt_6_sub_inst106_out[0]});
assign magma_Bits_8_lshr_inst54_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst108_out[2],magma_UInt_6_sub_inst108_out[1],magma_UInt_6_sub_inst108_out[0]});
assign magma_Bits_8_lshr_inst55_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst110_out[2],magma_UInt_6_sub_inst110_out[1],magma_UInt_6_sub_inst110_out[0]});
assign magma_Bits_8_lshr_inst56_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst112_out[2],magma_UInt_6_sub_inst112_out[1],magma_UInt_6_sub_inst112_out[0]});
assign magma_Bits_8_lshr_inst57_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst114_out[2],magma_UInt_6_sub_inst114_out[1],magma_UInt_6_sub_inst114_out[0]});
assign magma_Bits_8_lshr_inst58_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst116_out[2],magma_UInt_6_sub_inst116_out[1],magma_UInt_6_sub_inst116_out[0]});
assign magma_Bits_8_lshr_inst59_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst118_out[2],magma_UInt_6_sub_inst118_out[1],magma_UInt_6_sub_inst118_out[0]});
assign magma_Bits_8_lshr_inst6_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst12_out[2],magma_UInt_6_sub_inst12_out[1],magma_UInt_6_sub_inst12_out[0]});
assign magma_Bits_8_lshr_inst60_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst120_out[2],magma_UInt_6_sub_inst120_out[1],magma_UInt_6_sub_inst120_out[0]});
assign magma_Bits_8_lshr_inst61_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst122_out[2],magma_UInt_6_sub_inst122_out[1],magma_UInt_6_sub_inst122_out[0]});
assign magma_Bits_8_lshr_inst62_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst124_out[2],magma_UInt_6_sub_inst124_out[1],magma_UInt_6_sub_inst124_out[0]});
assign magma_Bits_8_lshr_inst63_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst126_out[2],magma_UInt_6_sub_inst126_out[1],magma_UInt_6_sub_inst126_out[0]});
assign magma_Bits_8_lshr_inst7_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst14_out[2],magma_UInt_6_sub_inst14_out[1],magma_UInt_6_sub_inst14_out[0]});
assign magma_Bits_8_lshr_inst8_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst16_out[2],magma_UInt_6_sub_inst16_out[1],magma_UInt_6_sub_inst16_out[0]});
assign magma_Bits_8_lshr_inst9_out = write_data >> ({1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_6_sub_inst18_out[2],magma_UInt_6_sub_inst18_out[1],magma_UInt_6_sub_inst18_out[0]});
assign magma_UInt_6_mul_inst0_out = 6'(({1'b0,1'b0,1'b0,read_addr}) * 6'h08);
assign magma_UInt_6_mul_inst1_out = 6'(({1'b0,1'b0,1'b0,write_addr}) * 6'h08);
assign magma_UInt_6_sub_inst0_out = 6'(6'h00 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst10_out = 6'(6'h05 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst100_out = 6'(6'h32 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst102_out = 6'(6'h33 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst104_out = 6'(6'h34 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst106_out = 6'(6'h35 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst108_out = 6'(6'h36 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst110_out = 6'(6'h37 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst112_out = 6'(6'h38 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst114_out = 6'(6'h39 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst116_out = 6'(6'h3a - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst118_out = 6'(6'h3b - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst12_out = 6'(6'h06 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst120_out = 6'(6'h3c - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst122_out = 6'(6'h3d - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst124_out = 6'(6'h3e - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst126_out = 6'(6'h3f - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst14_out = 6'(6'h07 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst16_out = 6'(6'h08 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst18_out = 6'(6'h09 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst2_out = 6'(6'h01 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst20_out = 6'(6'h0a - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst22_out = 6'(6'h0b - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst24_out = 6'(6'h0c - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst26_out = 6'(6'h0d - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst28_out = 6'(6'h0e - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst30_out = 6'(6'h0f - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst32_out = 6'(6'h10 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst34_out = 6'(6'h11 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst36_out = 6'(6'h12 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst38_out = 6'(6'h13 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst4_out = 6'(6'h02 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst40_out = 6'(6'h14 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst42_out = 6'(6'h15 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst44_out = 6'(6'h16 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst46_out = 6'(6'h17 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst48_out = 6'(6'h18 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst50_out = 6'(6'h19 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst52_out = 6'(6'h1a - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst54_out = 6'(6'h1b - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst56_out = 6'(6'h1c - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst58_out = 6'(6'h1d - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst6_out = 6'(6'h03 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst60_out = 6'(6'h1e - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst62_out = 6'(6'h1f - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst64_out = 6'(6'h20 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst66_out = 6'(6'h21 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst68_out = 6'(6'h22 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst70_out = 6'(6'h23 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst72_out = 6'(6'h24 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst74_out = 6'(6'h25 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst76_out = 6'(6'h26 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst78_out = 6'(6'h27 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst8_out = 6'(6'h04 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst80_out = 6'(6'h28 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst82_out = 6'(6'h29 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst84_out = 6'(6'h2a - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst86_out = 6'(6'h2b - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst88_out = 6'(6'h2c - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst90_out = 6'(6'h2d - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst92_out = 6'(6'h2e - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst94_out = 6'(6'h2f - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst96_out = 6'(6'h30 - magma_UInt_6_mul_inst1_out);
assign magma_UInt_6_sub_inst98_out = 6'(6'h31 - magma_UInt_6_mul_inst1_out);
endmodule

