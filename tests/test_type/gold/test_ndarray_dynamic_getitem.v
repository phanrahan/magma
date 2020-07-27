module mantle_wire__typeBitIn6 (
    output [5:0] in,
    input [5:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBitIn2 (
    output [1:0] in,
    input [1:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit6 (
    input [5:0] in,
    output [5:0] out
);
assign out = in;
endmodule

module mantle_wire__typeBit2 (
    input [1:0] in,
    output [1:0] out
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
    input [1:0] I_0_0,
    input [1:0] I_0_1,
    input [1:0] I_0_2,
    input [1:0] I_1_0,
    input [1:0] I_1_1,
    input [1:0] I_1_2,
    input [1:0] I_2_0,
    input [1:0] I_2_1,
    input [1:0] I_2_2,
    input [1:0] I_3_0,
    input [1:0] I_3_1,
    input [1:0] I_3_2,
    output [1:0] O_0_0,
    output [1:0] O_0_1,
    output [1:0] O_0_2,
    output [1:0] O_1_0,
    output [1:0] O_1_1,
    output [1:0] O_1_2,
    output [1:0] O_2_0,
    output [1:0] O_2_1,
    output [1:0] O_2_2,
    output [1:0] O_3_0,
    output [1:0] O_3_1,
    output [1:0] O_3_2
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
wire [23:0] reg_P_inst0_out;
mantle_wire__typeBit2 _$_U11 (
    .in(I_0_0),
    .out(_$_U11_out)
);
mantle_wire__typeBit2 _$_U12 (
    .in(I_0_1),
    .out(_$_U12_out)
);
mantle_wire__typeBit2 _$_U13 (
    .in(I_0_2),
    .out(_$_U13_out)
);
mantle_wire__typeBit2 _$_U14 (
    .in(I_1_0),
    .out(_$_U14_out)
);
mantle_wire__typeBit2 _$_U15 (
    .in(I_1_1),
    .out(_$_U15_out)
);
mantle_wire__typeBit2 _$_U16 (
    .in(I_1_2),
    .out(_$_U16_out)
);
mantle_wire__typeBit2 _$_U17 (
    .in(I_2_0),
    .out(_$_U17_out)
);
mantle_wire__typeBit2 _$_U18 (
    .in(I_2_1),
    .out(_$_U18_out)
);
mantle_wire__typeBit2 _$_U19 (
    .in(I_2_2),
    .out(_$_U19_out)
);
mantle_wire__typeBit2 _$_U20 (
    .in(I_3_0),
    .out(_$_U20_out)
);
mantle_wire__typeBit2 _$_U21 (
    .in(I_3_1),
    .out(_$_U21_out)
);
mantle_wire__typeBit2 _$_U22 (
    .in(I_3_2),
    .out(_$_U22_out)
);
mantle_wire__typeBitIn2 _$_U23 (
    .in(O_0_0),
    .out(reg_P_inst0_out[1:0])
);
mantle_wire__typeBitIn2 _$_U24 (
    .in(O_0_1),
    .out(reg_P_inst0_out[3:2])
);
mantle_wire__typeBitIn2 _$_U25 (
    .in(O_0_2),
    .out(reg_P_inst0_out[5:4])
);
mantle_wire__typeBitIn2 _$_U26 (
    .in(O_1_0),
    .out(reg_P_inst0_out[7:6])
);
mantle_wire__typeBitIn2 _$_U27 (
    .in(O_1_1),
    .out(reg_P_inst0_out[9:8])
);
mantle_wire__typeBitIn2 _$_U28 (
    .in(O_1_2),
    .out(reg_P_inst0_out[11:10])
);
mantle_wire__typeBitIn2 _$_U29 (
    .in(O_2_0),
    .out(reg_P_inst0_out[13:12])
);
mantle_wire__typeBitIn2 _$_U30 (
    .in(O_2_1),
    .out(reg_P_inst0_out[15:14])
);
mantle_wire__typeBitIn2 _$_U31 (
    .in(O_2_2),
    .out(reg_P_inst0_out[17:16])
);
mantle_wire__typeBitIn2 _$_U32 (
    .in(O_3_0),
    .out(reg_P_inst0_out[19:18])
);
mantle_wire__typeBitIn2 _$_U33 (
    .in(O_3_1),
    .out(reg_P_inst0_out[21:20])
);
mantle_wire__typeBitIn2 _$_U34 (
    .in(O_3_2),
    .out(reg_P_inst0_out[23:22])
);
coreir_reg #(
    .clk_posedge(1'b1),
    .init(24'h000000),
    .width(24)
) reg_P_inst0 (
    .clk(CLK),
    .in({_$_U22_out[1:0],_$_U21_out[1:0],_$_U20_out[1:0],_$_U19_out[1:0],_$_U18_out[1:0],_$_U17_out[1:0],_$_U16_out[1:0],_$_U15_out[1:0],_$_U14_out[1:0],_$_U13_out[1:0],_$_U12_out[1:0],_$_U11_out[1:0]}),
    .out(reg_P_inst0_out)
);
endmodule

module Mux4xArray3_Array2_OutBit (
    input [1:0] I0_0,
    input [1:0] I0_1,
    input [1:0] I0_2,
    input [1:0] I1_0,
    input [1:0] I1_1,
    input [1:0] I1_2,
    input [1:0] I2_0,
    input [1:0] I2_1,
    input [1:0] I2_2,
    input [1:0] I3_0,
    input [1:0] I3_1,
    input [1:0] I3_2,
    output [1:0] O_0,
    output [1:0] O_1,
    output [1:0] O_2,
    input [1:0] S
);
wire [1:0] _$_U37_out;
wire [1:0] _$_U38_out;
wire [1:0] _$_U39_out;
wire [1:0] _$_U40_out;
wire [1:0] _$_U41_out;
wire [1:0] _$_U42_out;
wire [1:0] _$_U43_out;
wire [1:0] _$_U44_out;
wire [1:0] _$_U45_out;
wire [1:0] _$_U46_out;
wire [1:0] _$_U47_out;
wire [1:0] _$_U48_out;
wire [5:0] _$_U5_in;
wire [5:0] _$_U6_in;
wire [5:0] _$_U7_in;
wire [5:0] _$_U8_in;
wire [5:0] _$_U9_out;
reg [5:0] coreir_commonlib_mux4x6_inst0_out;
mantle_wire__typeBit2 _$_U37 (
    .in(I0_0),
    .out(_$_U37_out)
);
mantle_wire__typeBit2 _$_U38 (
    .in(I0_1),
    .out(_$_U38_out)
);
mantle_wire__typeBit2 _$_U39 (
    .in(I0_2),
    .out(_$_U39_out)
);
mantle_wire__typeBit2 _$_U40 (
    .in(I1_0),
    .out(_$_U40_out)
);
mantle_wire__typeBit2 _$_U41 (
    .in(I1_1),
    .out(_$_U41_out)
);
mantle_wire__typeBit2 _$_U42 (
    .in(I1_2),
    .out(_$_U42_out)
);
mantle_wire__typeBit2 _$_U43 (
    .in(I2_0),
    .out(_$_U43_out)
);
mantle_wire__typeBit2 _$_U44 (
    .in(I2_1),
    .out(_$_U44_out)
);
mantle_wire__typeBit2 _$_U45 (
    .in(I2_2),
    .out(_$_U45_out)
);
mantle_wire__typeBit2 _$_U46 (
    .in(I3_0),
    .out(_$_U46_out)
);
mantle_wire__typeBit2 _$_U47 (
    .in(I3_1),
    .out(_$_U47_out)
);
mantle_wire__typeBit2 _$_U48 (
    .in(I3_2),
    .out(_$_U48_out)
);
mantle_wire__typeBitIn2 _$_U49 (
    .in(O_0),
    .out(_$_U9_out[1:0])
);
mantle_wire__typeBitIn6 _$_U5 (
    .in(_$_U5_in),
    .out({_$_U39_out[1:0],_$_U38_out[1:0],_$_U37_out[1:0]})
);
mantle_wire__typeBitIn2 _$_U50 (
    .in(O_1),
    .out(_$_U9_out[3:2])
);
mantle_wire__typeBitIn2 _$_U51 (
    .in(O_2),
    .out(_$_U9_out[5:4])
);
mantle_wire__typeBitIn6 _$_U6 (
    .in(_$_U6_in),
    .out({_$_U42_out[1:0],_$_U41_out[1:0],_$_U40_out[1:0]})
);
mantle_wire__typeBitIn6 _$_U7 (
    .in(_$_U7_in),
    .out({_$_U45_out[1:0],_$_U44_out[1:0],_$_U43_out[1:0]})
);
mantle_wire__typeBitIn6 _$_U8 (
    .in(_$_U8_in),
    .out({_$_U48_out[1:0],_$_U47_out[1:0],_$_U46_out[1:0]})
);
mantle_wire__typeBit6 _$_U9 (
    .in(coreir_commonlib_mux4x6_inst0_out),
    .out(_$_U9_out)
);
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux4x6_inst0_out = _$_U5_in;
end else if (S == 1) begin
    coreir_commonlib_mux4x6_inst0_out = _$_U6_in;
end else if (S == 2) begin
    coreir_commonlib_mux4x6_inst0_out = _$_U7_in;
end else begin
    coreir_commonlib_mux4x6_inst0_out = _$_U8_in;
end
end

endmodule

module Main (
    input CLK,
    input [1:0] raddr,
    output [1:0] rdata_0,
    output [1:0] rdata_1,
    output [1:0] rdata_2
);
wire [1:0] Register_inst0_O_0_0;
wire [1:0] Register_inst0_O_0_1;
wire [1:0] Register_inst0_O_0_2;
wire [1:0] Register_inst0_O_1_0;
wire [1:0] Register_inst0_O_1_1;
wire [1:0] Register_inst0_O_1_2;
wire [1:0] Register_inst0_O_2_0;
wire [1:0] Register_inst0_O_2_1;
wire [1:0] Register_inst0_O_2_2;
wire [1:0] Register_inst0_O_3_0;
wire [1:0] Register_inst0_O_3_1;
wire [1:0] Register_inst0_O_3_2;
Mux4xArray3_Array2_OutBit Mux4xArray3_Array2_OutBit_inst0 (
    .I0_0(Register_inst0_O_0_0),
    .I0_1(Register_inst0_O_0_1),
    .I0_2(Register_inst0_O_0_2),
    .I1_0(Register_inst0_O_1_0),
    .I1_1(Register_inst0_O_1_1),
    .I1_2(Register_inst0_O_1_2),
    .I2_0(Register_inst0_O_2_0),
    .I2_1(Register_inst0_O_2_1),
    .I2_2(Register_inst0_O_2_2),
    .I3_0(Register_inst0_O_3_0),
    .I3_1(Register_inst0_O_3_1),
    .I3_2(Register_inst0_O_3_2),
    .O_0(rdata_0),
    .O_1(rdata_1),
    .O_2(rdata_2),
    .S(raddr)
);
Register Register_inst0 (
    .CLK(CLK),
    .I_0_0(Register_inst0_O_0_0),
    .I_0_1(Register_inst0_O_0_1),
    .I_0_2(Register_inst0_O_0_2),
    .I_1_0(Register_inst0_O_1_0),
    .I_1_1(Register_inst0_O_1_1),
    .I_1_2(Register_inst0_O_1_2),
    .I_2_0(Register_inst0_O_2_0),
    .I_2_1(Register_inst0_O_2_1),
    .I_2_2(Register_inst0_O_2_2),
    .I_3_0(Register_inst0_O_3_0),
    .I_3_1(Register_inst0_O_3_1),
    .I_3_2(Register_inst0_O_3_2),
    .O_0_0(Register_inst0_O_0_0),
    .O_0_1(Register_inst0_O_0_1),
    .O_0_2(Register_inst0_O_0_2),
    .O_1_0(Register_inst0_O_1_0),
    .O_1_1(Register_inst0_O_1_1),
    .O_1_2(Register_inst0_O_1_2),
    .O_2_0(Register_inst0_O_2_0),
    .O_2_1(Register_inst0_O_2_1),
    .O_2_2(Register_inst0_O_2_2),
    .O_3_0(Register_inst0_O_3_0),
    .O_3_1(Register_inst0_O_3_1),
    .O_3_2(Register_inst0_O_3_2)
);
endmodule

