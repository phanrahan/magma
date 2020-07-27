module mantle_wire__typeBitIn2 (
    output [1:0] in,
    input [1:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBitIn12 (
    output [11:0] in,
    input [11:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit2 (
    input [1:0] in,
    output [1:0] out
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

module Register (
    input CLK,
    input [1:0] I_0_0_0,
    input [1:0] I_0_0_1,
    input [1:0] I_0_0_2,
    input [1:0] I_0_1_0,
    input [1:0] I_0_1_1,
    input [1:0] I_0_1_2,
    input [1:0] I_1_0_0,
    input [1:0] I_1_0_1,
    input [1:0] I_1_0_2,
    input [1:0] I_1_1_0,
    input [1:0] I_1_1_1,
    input [1:0] I_1_1_2,
    input [1:0] I_2_0_0,
    input [1:0] I_2_0_1,
    input [1:0] I_2_0_2,
    input [1:0] I_2_1_0,
    input [1:0] I_2_1_1,
    input [1:0] I_2_1_2,
    input [1:0] I_3_0_0,
    input [1:0] I_3_0_1,
    input [1:0] I_3_0_2,
    input [1:0] I_3_1_0,
    input [1:0] I_3_1_1,
    input [1:0] I_3_1_2,
    output [1:0] O_0_0_0,
    output [1:0] O_0_0_1,
    output [1:0] O_0_0_2,
    output [1:0] O_0_1_0,
    output [1:0] O_0_1_1,
    output [1:0] O_0_1_2,
    output [1:0] O_1_0_0,
    output [1:0] O_1_0_1,
    output [1:0] O_1_0_2,
    output [1:0] O_1_1_0,
    output [1:0] O_1_1_1,
    output [1:0] O_1_1_2,
    output [1:0] O_2_0_0,
    output [1:0] O_2_0_1,
    output [1:0] O_2_0_2,
    output [1:0] O_2_1_0,
    output [1:0] O_2_1_1,
    output [1:0] O_2_1_2,
    output [1:0] O_3_0_0,
    output [1:0] O_3_0_1,
    output [1:0] O_3_0_2,
    output [1:0] O_3_1_0,
    output [1:0] O_3_1_1,
    output [1:0] O_3_1_2
);
wire [1:0] _$_U11_out;
wire [1:0] _$_U12_out;
wire [1:0] _$_U13_out;
wire [1:0] _$_U14_out;
wire [1:0] _$_U15_out;
wire [1:0] _$_U16_out;
wire [1:0] _$_U17_out;
wire [1:0] _$_U18_out;
wire [1:0] _$_U19_out;
wire [1:0] _$_U20_out;
wire [1:0] _$_U21_out;
wire [1:0] _$_U22_out;
wire [1:0] _$_U23_out;
wire [1:0] _$_U24_out;
wire [1:0] _$_U25_out;
wire [1:0] _$_U26_out;
wire [1:0] _$_U27_out;
wire [1:0] _$_U28_out;
wire [1:0] _$_U29_out;
wire [1:0] _$_U30_out;
wire [1:0] _$_U31_out;
wire [1:0] _$_U32_out;
wire [1:0] _$_U33_out;
wire [1:0] _$_U34_out;
wire [47:0] reg_P_inst0_out;
mantle_wire__typeBit2 _$_U11 (
    .in(I_0_0_0),
    .out(_$_U11_out)
);
mantle_wire__typeBit2 _$_U12 (
    .in(I_0_0_1),
    .out(_$_U12_out)
);
mantle_wire__typeBit2 _$_U13 (
    .in(I_0_0_2),
    .out(_$_U13_out)
);
mantle_wire__typeBit2 _$_U14 (
    .in(I_0_1_0),
    .out(_$_U14_out)
);
mantle_wire__typeBit2 _$_U15 (
    .in(I_0_1_1),
    .out(_$_U15_out)
);
mantle_wire__typeBit2 _$_U16 (
    .in(I_0_1_2),
    .out(_$_U16_out)
);
mantle_wire__typeBit2 _$_U17 (
    .in(I_1_0_0),
    .out(_$_U17_out)
);
mantle_wire__typeBit2 _$_U18 (
    .in(I_1_0_1),
    .out(_$_U18_out)
);
mantle_wire__typeBit2 _$_U19 (
    .in(I_1_0_2),
    .out(_$_U19_out)
);
mantle_wire__typeBit2 _$_U20 (
    .in(I_1_1_0),
    .out(_$_U20_out)
);
mantle_wire__typeBit2 _$_U21 (
    .in(I_1_1_1),
    .out(_$_U21_out)
);
mantle_wire__typeBit2 _$_U22 (
    .in(I_1_1_2),
    .out(_$_U22_out)
);
mantle_wire__typeBit2 _$_U23 (
    .in(I_2_0_0),
    .out(_$_U23_out)
);
mantle_wire__typeBit2 _$_U24 (
    .in(I_2_0_1),
    .out(_$_U24_out)
);
mantle_wire__typeBit2 _$_U25 (
    .in(I_2_0_2),
    .out(_$_U25_out)
);
mantle_wire__typeBit2 _$_U26 (
    .in(I_2_1_0),
    .out(_$_U26_out)
);
mantle_wire__typeBit2 _$_U27 (
    .in(I_2_1_1),
    .out(_$_U27_out)
);
mantle_wire__typeBit2 _$_U28 (
    .in(I_2_1_2),
    .out(_$_U28_out)
);
mantle_wire__typeBit2 _$_U29 (
    .in(I_3_0_0),
    .out(_$_U29_out)
);
mantle_wire__typeBit2 _$_U30 (
    .in(I_3_0_1),
    .out(_$_U30_out)
);
mantle_wire__typeBit2 _$_U31 (
    .in(I_3_0_2),
    .out(_$_U31_out)
);
mantle_wire__typeBit2 _$_U32 (
    .in(I_3_1_0),
    .out(_$_U32_out)
);
mantle_wire__typeBit2 _$_U33 (
    .in(I_3_1_1),
    .out(_$_U33_out)
);
mantle_wire__typeBit2 _$_U34 (
    .in(I_3_1_2),
    .out(_$_U34_out)
);
mantle_wire__typeBitIn2 _$_U35 (
    .in(O_0_0_0),
    .out(reg_P_inst0_out[1:0])
);
mantle_wire__typeBitIn2 _$_U36 (
    .in(O_0_0_1),
    .out(reg_P_inst0_out[3:2])
);
mantle_wire__typeBitIn2 _$_U37 (
    .in(O_0_0_2),
    .out(reg_P_inst0_out[5:4])
);
mantle_wire__typeBitIn2 _$_U38 (
    .in(O_0_1_0),
    .out(reg_P_inst0_out[7:6])
);
mantle_wire__typeBitIn2 _$_U39 (
    .in(O_0_1_1),
    .out(reg_P_inst0_out[9:8])
);
mantle_wire__typeBitIn2 _$_U40 (
    .in(O_0_1_2),
    .out(reg_P_inst0_out[11:10])
);
mantle_wire__typeBitIn2 _$_U41 (
    .in(O_1_0_0),
    .out(reg_P_inst0_out[13:12])
);
mantle_wire__typeBitIn2 _$_U42 (
    .in(O_1_0_1),
    .out(reg_P_inst0_out[15:14])
);
mantle_wire__typeBitIn2 _$_U43 (
    .in(O_1_0_2),
    .out(reg_P_inst0_out[17:16])
);
mantle_wire__typeBitIn2 _$_U44 (
    .in(O_1_1_0),
    .out(reg_P_inst0_out[19:18])
);
mantle_wire__typeBitIn2 _$_U45 (
    .in(O_1_1_1),
    .out(reg_P_inst0_out[21:20])
);
mantle_wire__typeBitIn2 _$_U46 (
    .in(O_1_1_2),
    .out(reg_P_inst0_out[23:22])
);
mantle_wire__typeBitIn2 _$_U47 (
    .in(O_2_0_0),
    .out(reg_P_inst0_out[25:24])
);
mantle_wire__typeBitIn2 _$_U48 (
    .in(O_2_0_1),
    .out(reg_P_inst0_out[27:26])
);
mantle_wire__typeBitIn2 _$_U49 (
    .in(O_2_0_2),
    .out(reg_P_inst0_out[29:28])
);
mantle_wire__typeBitIn2 _$_U50 (
    .in(O_2_1_0),
    .out(reg_P_inst0_out[31:30])
);
mantle_wire__typeBitIn2 _$_U51 (
    .in(O_2_1_1),
    .out(reg_P_inst0_out[33:32])
);
mantle_wire__typeBitIn2 _$_U52 (
    .in(O_2_1_2),
    .out(reg_P_inst0_out[35:34])
);
mantle_wire__typeBitIn2 _$_U53 (
    .in(O_3_0_0),
    .out(reg_P_inst0_out[37:36])
);
mantle_wire__typeBitIn2 _$_U54 (
    .in(O_3_0_1),
    .out(reg_P_inst0_out[39:38])
);
mantle_wire__typeBitIn2 _$_U55 (
    .in(O_3_0_2),
    .out(reg_P_inst0_out[41:40])
);
mantle_wire__typeBitIn2 _$_U56 (
    .in(O_3_1_0),
    .out(reg_P_inst0_out[43:42])
);
mantle_wire__typeBitIn2 _$_U57 (
    .in(O_3_1_1),
    .out(reg_P_inst0_out[45:44])
);
mantle_wire__typeBitIn2 _$_U58 (
    .in(O_3_1_2),
    .out(reg_P_inst0_out[47:46])
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(48'h000000000000),
    .width(48)
) reg_P_inst0 (
    .clk(CLK),
    .in({_$_U34_out[1:0],_$_U33_out[1:0],_$_U32_out[1:0],_$_U31_out[1:0],_$_U30_out[1:0],_$_U29_out[1:0],_$_U28_out[1:0],_$_U27_out[1:0],_$_U26_out[1:0],_$_U25_out[1:0],_$_U24_out[1:0],_$_U23_out[1:0],_$_U22_out[1:0],_$_U21_out[1:0],_$_U20_out[1:0],_$_U19_out[1:0],_$_U18_out[1:0],_$_U17_out[1:0],_$_U16_out[1:0],_$_U15_out[1:0],_$_U14_out[1:0],_$_U13_out[1:0],_$_U12_out[1:0],_$_U11_out[1:0]}),
    .out(reg_P_inst0_out)
);
endmodule

module Mux4xArray2_Array3_Array2_OutBit (
    input [1:0] I0_0_0,
    input [1:0] I0_0_1,
    input [1:0] I0_0_2,
    input [1:0] I0_1_0,
    input [1:0] I0_1_1,
    input [1:0] I0_1_2,
    input [1:0] I1_0_0,
    input [1:0] I1_0_1,
    input [1:0] I1_0_2,
    input [1:0] I1_1_0,
    input [1:0] I1_1_1,
    input [1:0] I1_1_2,
    input [1:0] I2_0_0,
    input [1:0] I2_0_1,
    input [1:0] I2_0_2,
    input [1:0] I2_1_0,
    input [1:0] I2_1_1,
    input [1:0] I2_1_2,
    input [1:0] I3_0_0,
    input [1:0] I3_0_1,
    input [1:0] I3_0_2,
    input [1:0] I3_1_0,
    input [1:0] I3_1_1,
    input [1:0] I3_1_2,
    output [1:0] O_0_0,
    output [1:0] O_0_1,
    output [1:0] O_0_2,
    output [1:0] O_1_0,
    output [1:0] O_1_1,
    output [1:0] O_1_2,
    input [1:0] S
);
wire [11:0] _$_U5_in;
wire [11:0] _$_U6_in;
wire [1:0] _$_U61_out;
wire [1:0] _$_U62_out;
wire [1:0] _$_U63_out;
wire [1:0] _$_U64_out;
wire [1:0] _$_U65_out;
wire [1:0] _$_U66_out;
wire [1:0] _$_U67_out;
wire [1:0] _$_U68_out;
wire [1:0] _$_U69_out;
wire [11:0] _$_U7_in;
wire [1:0] _$_U70_out;
wire [1:0] _$_U71_out;
wire [1:0] _$_U72_out;
wire [1:0] _$_U73_out;
wire [1:0] _$_U74_out;
wire [1:0] _$_U75_out;
wire [1:0] _$_U76_out;
wire [1:0] _$_U77_out;
wire [1:0] _$_U78_out;
wire [1:0] _$_U79_out;
wire [11:0] _$_U8_in;
wire [1:0] _$_U80_out;
wire [1:0] _$_U81_out;
wire [1:0] _$_U82_out;
wire [1:0] _$_U83_out;
wire [1:0] _$_U84_out;
wire [11:0] _$_U9_out;
reg [11:0] coreir_commonlib_mux4x12_inst0_out;
mantle_wire__typeBitIn12 _$_U5 (
    .in(_$_U5_in),
    .out({_$_U66_out[1:0],_$_U65_out[1:0],_$_U64_out[1:0],_$_U63_out[1:0],_$_U62_out[1:0],_$_U61_out[1:0]})
);
mantle_wire__typeBitIn12 _$_U6 (
    .in(_$_U6_in),
    .out({_$_U72_out[1:0],_$_U71_out[1:0],_$_U70_out[1:0],_$_U69_out[1:0],_$_U68_out[1:0],_$_U67_out[1:0]})
);
mantle_wire__typeBit2 _$_U61 (
    .in(I0_0_0),
    .out(_$_U61_out)
);
mantle_wire__typeBit2 _$_U62 (
    .in(I0_0_1),
    .out(_$_U62_out)
);
mantle_wire__typeBit2 _$_U63 (
    .in(I0_0_2),
    .out(_$_U63_out)
);
mantle_wire__typeBit2 _$_U64 (
    .in(I0_1_0),
    .out(_$_U64_out)
);
mantle_wire__typeBit2 _$_U65 (
    .in(I0_1_1),
    .out(_$_U65_out)
);
mantle_wire__typeBit2 _$_U66 (
    .in(I0_1_2),
    .out(_$_U66_out)
);
mantle_wire__typeBit2 _$_U67 (
    .in(I1_0_0),
    .out(_$_U67_out)
);
mantle_wire__typeBit2 _$_U68 (
    .in(I1_0_1),
    .out(_$_U68_out)
);
mantle_wire__typeBit2 _$_U69 (
    .in(I1_0_2),
    .out(_$_U69_out)
);
mantle_wire__typeBitIn12 _$_U7 (
    .in(_$_U7_in),
    .out({_$_U78_out[1:0],_$_U77_out[1:0],_$_U76_out[1:0],_$_U75_out[1:0],_$_U74_out[1:0],_$_U73_out[1:0]})
);
mantle_wire__typeBit2 _$_U70 (
    .in(I1_1_0),
    .out(_$_U70_out)
);
mantle_wire__typeBit2 _$_U71 (
    .in(I1_1_1),
    .out(_$_U71_out)
);
mantle_wire__typeBit2 _$_U72 (
    .in(I1_1_2),
    .out(_$_U72_out)
);
mantle_wire__typeBit2 _$_U73 (
    .in(I2_0_0),
    .out(_$_U73_out)
);
mantle_wire__typeBit2 _$_U74 (
    .in(I2_0_1),
    .out(_$_U74_out)
);
mantle_wire__typeBit2 _$_U75 (
    .in(I2_0_2),
    .out(_$_U75_out)
);
mantle_wire__typeBit2 _$_U76 (
    .in(I2_1_0),
    .out(_$_U76_out)
);
mantle_wire__typeBit2 _$_U77 (
    .in(I2_1_1),
    .out(_$_U77_out)
);
mantle_wire__typeBit2 _$_U78 (
    .in(I2_1_2),
    .out(_$_U78_out)
);
mantle_wire__typeBit2 _$_U79 (
    .in(I3_0_0),
    .out(_$_U79_out)
);
mantle_wire__typeBitIn12 _$_U8 (
    .in(_$_U8_in),
    .out({_$_U84_out[1:0],_$_U83_out[1:0],_$_U82_out[1:0],_$_U81_out[1:0],_$_U80_out[1:0],_$_U79_out[1:0]})
);
mantle_wire__typeBit2 _$_U80 (
    .in(I3_0_1),
    .out(_$_U80_out)
);
mantle_wire__typeBit2 _$_U81 (
    .in(I3_0_2),
    .out(_$_U81_out)
);
mantle_wire__typeBit2 _$_U82 (
    .in(I3_1_0),
    .out(_$_U82_out)
);
mantle_wire__typeBit2 _$_U83 (
    .in(I3_1_1),
    .out(_$_U83_out)
);
mantle_wire__typeBit2 _$_U84 (
    .in(I3_1_2),
    .out(_$_U84_out)
);
mantle_wire__typeBitIn2 _$_U85 (
    .in(O_0_0),
    .out(_$_U9_out[1:0])
);
mantle_wire__typeBitIn2 _$_U86 (
    .in(O_0_1),
    .out(_$_U9_out[3:2])
);
mantle_wire__typeBitIn2 _$_U87 (
    .in(O_0_2),
    .out(_$_U9_out[5:4])
);
mantle_wire__typeBitIn2 _$_U88 (
    .in(O_1_0),
    .out(_$_U9_out[7:6])
);
mantle_wire__typeBitIn2 _$_U89 (
    .in(O_1_1),
    .out(_$_U9_out[9:8])
);
mantle_wire__typeBit12 _$_U9 (
    .in(coreir_commonlib_mux4x12_inst0_out),
    .out(_$_U9_out)
);
mantle_wire__typeBitIn2 _$_U90 (
    .in(O_1_2),
    .out(_$_U9_out[11:10])
);
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux4x12_inst0_out = _$_U5_in;
end else if (S == 1) begin
    coreir_commonlib_mux4x12_inst0_out = _$_U6_in;
end else if (S == 2) begin
    coreir_commonlib_mux4x12_inst0_out = _$_U7_in;
end else begin
    coreir_commonlib_mux4x12_inst0_out = _$_U8_in;
end
end

endmodule

module Main (
    input CLK,
    input [1:0] raddr0,
    input [1:0] raddr1,
    output [1:0] rdata0_0,
    output [1:0] rdata0_1,
    output [1:0] rdata0_2,
    output [1:0] rdata1_0,
    output [1:0] rdata1_1,
    output [1:0] rdata1_2
);
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_0;
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_1;
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_2;
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_0;
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_1;
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_2;
wire [1:0] Register_inst0_O_0_0_0;
wire [1:0] Register_inst0_O_0_0_1;
wire [1:0] Register_inst0_O_0_0_2;
wire [1:0] Register_inst0_O_0_1_0;
wire [1:0] Register_inst0_O_0_1_1;
wire [1:0] Register_inst0_O_0_1_2;
wire [1:0] Register_inst0_O_1_0_0;
wire [1:0] Register_inst0_O_1_0_1;
wire [1:0] Register_inst0_O_1_0_2;
wire [1:0] Register_inst0_O_1_1_0;
wire [1:0] Register_inst0_O_1_1_1;
wire [1:0] Register_inst0_O_1_1_2;
wire [1:0] Register_inst0_O_2_0_0;
wire [1:0] Register_inst0_O_2_0_1;
wire [1:0] Register_inst0_O_2_0_2;
wire [1:0] Register_inst0_O_2_1_0;
wire [1:0] Register_inst0_O_2_1_1;
wire [1:0] Register_inst0_O_2_1_2;
wire [1:0] Register_inst0_O_3_0_0;
wire [1:0] Register_inst0_O_3_0_1;
wire [1:0] Register_inst0_O_3_0_2;
wire [1:0] Register_inst0_O_3_1_0;
wire [1:0] Register_inst0_O_3_1_1;
wire [1:0] Register_inst0_O_3_1_2;
Mux4xArray2_Array3_Array2_OutBit Mux4xArray2_Array3_Array2_OutBit_inst0 (
    .I0_0_0(Register_inst0_O_0_0_0),
    .I0_0_1(Register_inst0_O_0_0_1),
    .I0_0_2(Register_inst0_O_0_0_2),
    .I0_1_0(Register_inst0_O_0_1_0),
    .I0_1_1(Register_inst0_O_0_1_1),
    .I0_1_2(Register_inst0_O_0_1_2),
    .I1_0_0(Register_inst0_O_1_0_0),
    .I1_0_1(Register_inst0_O_1_0_1),
    .I1_0_2(Register_inst0_O_1_0_2),
    .I1_1_0(Register_inst0_O_1_1_0),
    .I1_1_1(Register_inst0_O_1_1_1),
    .I1_1_2(Register_inst0_O_1_1_2),
    .I2_0_0(Register_inst0_O_2_0_0),
    .I2_0_1(Register_inst0_O_2_0_1),
    .I2_0_2(Register_inst0_O_2_0_2),
    .I2_1_0(Register_inst0_O_2_1_0),
    .I2_1_1(Register_inst0_O_2_1_1),
    .I2_1_2(Register_inst0_O_2_1_2),
    .I3_0_0(Register_inst0_O_3_0_0),
    .I3_0_1(Register_inst0_O_3_0_1),
    .I3_0_2(Register_inst0_O_3_0_2),
    .I3_1_0(Register_inst0_O_3_1_0),
    .I3_1_1(Register_inst0_O_3_1_1),
    .I3_1_2(Register_inst0_O_3_1_2),
    .O_0_0(rdata0_0),
    .O_0_1(rdata0_1),
    .O_0_2(rdata0_2),
    .O_1_0(Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_0),
    .O_1_1(Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_1),
    .O_1_2(Mux4xArray2_Array3_Array2_OutBit_inst0_O_1_2),
    .S(raddr0)
);
Mux4xArray2_Array3_Array2_OutBit Mux4xArray2_Array3_Array2_OutBit_inst1 (
    .I0_0_0(Register_inst0_O_0_0_0),
    .I0_0_1(Register_inst0_O_0_0_1),
    .I0_0_2(Register_inst0_O_0_0_2),
    .I0_1_0(Register_inst0_O_0_1_0),
    .I0_1_1(Register_inst0_O_0_1_1),
    .I0_1_2(Register_inst0_O_0_1_2),
    .I1_0_0(Register_inst0_O_1_0_0),
    .I1_0_1(Register_inst0_O_1_0_1),
    .I1_0_2(Register_inst0_O_1_0_2),
    .I1_1_0(Register_inst0_O_1_1_0),
    .I1_1_1(Register_inst0_O_1_1_1),
    .I1_1_2(Register_inst0_O_1_1_2),
    .I2_0_0(Register_inst0_O_2_0_0),
    .I2_0_1(Register_inst0_O_2_0_1),
    .I2_0_2(Register_inst0_O_2_0_2),
    .I2_1_0(Register_inst0_O_2_1_0),
    .I2_1_1(Register_inst0_O_2_1_1),
    .I2_1_2(Register_inst0_O_2_1_2),
    .I3_0_0(Register_inst0_O_3_0_0),
    .I3_0_1(Register_inst0_O_3_0_1),
    .I3_0_2(Register_inst0_O_3_0_2),
    .I3_1_0(Register_inst0_O_3_1_0),
    .I3_1_1(Register_inst0_O_3_1_1),
    .I3_1_2(Register_inst0_O_3_1_2),
    .O_0_0(Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_0),
    .O_0_1(Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_1),
    .O_0_2(Mux4xArray2_Array3_Array2_OutBit_inst1_O_0_2),
    .O_1_0(rdata1_0),
    .O_1_1(rdata1_1),
    .O_1_2(rdata1_2),
    .S(raddr1)
);
Register Register_inst0 (
    .CLK(CLK),
    .I_0_0_0(Register_inst0_O_0_0_0),
    .I_0_0_1(Register_inst0_O_0_0_1),
    .I_0_0_2(Register_inst0_O_0_0_2),
    .I_0_1_0(Register_inst0_O_0_1_0),
    .I_0_1_1(Register_inst0_O_0_1_1),
    .I_0_1_2(Register_inst0_O_0_1_2),
    .I_1_0_0(Register_inst0_O_1_0_0),
    .I_1_0_1(Register_inst0_O_1_0_1),
    .I_1_0_2(Register_inst0_O_1_0_2),
    .I_1_1_0(Register_inst0_O_1_1_0),
    .I_1_1_1(Register_inst0_O_1_1_1),
    .I_1_1_2(Register_inst0_O_1_1_2),
    .I_2_0_0(Register_inst0_O_2_0_0),
    .I_2_0_1(Register_inst0_O_2_0_1),
    .I_2_0_2(Register_inst0_O_2_0_2),
    .I_2_1_0(Register_inst0_O_2_1_0),
    .I_2_1_1(Register_inst0_O_2_1_1),
    .I_2_1_2(Register_inst0_O_2_1_2),
    .I_3_0_0(Register_inst0_O_3_0_0),
    .I_3_0_1(Register_inst0_O_3_0_1),
    .I_3_0_2(Register_inst0_O_3_0_2),
    .I_3_1_0(Register_inst0_O_3_1_0),
    .I_3_1_1(Register_inst0_O_3_1_1),
    .I_3_1_2(Register_inst0_O_3_1_2),
    .O_0_0_0(Register_inst0_O_0_0_0),
    .O_0_0_1(Register_inst0_O_0_0_1),
    .O_0_0_2(Register_inst0_O_0_0_2),
    .O_0_1_0(Register_inst0_O_0_1_0),
    .O_0_1_1(Register_inst0_O_0_1_1),
    .O_0_1_2(Register_inst0_O_0_1_2),
    .O_1_0_0(Register_inst0_O_1_0_0),
    .O_1_0_1(Register_inst0_O_1_0_1),
    .O_1_0_2(Register_inst0_O_1_0_2),
    .O_1_1_0(Register_inst0_O_1_1_0),
    .O_1_1_1(Register_inst0_O_1_1_1),
    .O_1_1_2(Register_inst0_O_1_1_2),
    .O_2_0_0(Register_inst0_O_2_0_0),
    .O_2_0_1(Register_inst0_O_2_0_1),
    .O_2_0_2(Register_inst0_O_2_0_2),
    .O_2_1_0(Register_inst0_O_2_1_0),
    .O_2_1_1(Register_inst0_O_2_1_1),
    .O_2_1_2(Register_inst0_O_2_1_2),
    .O_3_0_0(Register_inst0_O_3_0_0),
    .O_3_0_1(Register_inst0_O_3_0_1),
    .O_3_0_2(Register_inst0_O_3_0_2),
    .O_3_1_0(Register_inst0_O_3_1_0),
    .O_3_1_1(Register_inst0_O_3_1_1),
    .O_3_1_2(Register_inst0_O_3_1_2)
);
endmodule

