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
wire [11:0] _$_U5_in;
wire [11:0] _$_U6_in;
wire [11:0] _$_U7_in;
wire [11:0] _$_U8_in;
wire [11:0] _$_U9_out;
reg [11:0] coreir_commonlib_mux4x12_inst0_out;
mantle_wire__typeBit2 _$_U11 (
    .in(I0_0_0),
    .out(_$_U11_out)
);
mantle_wire__typeBit2 _$_U12 (
    .in(I0_0_1),
    .out(_$_U12_out)
);
mantle_wire__typeBit2 _$_U13 (
    .in(I0_0_2),
    .out(_$_U13_out)
);
mantle_wire__typeBit2 _$_U14 (
    .in(I0_1_0),
    .out(_$_U14_out)
);
mantle_wire__typeBit2 _$_U15 (
    .in(I0_1_1),
    .out(_$_U15_out)
);
mantle_wire__typeBit2 _$_U16 (
    .in(I0_1_2),
    .out(_$_U16_out)
);
mantle_wire__typeBit2 _$_U17 (
    .in(I1_0_0),
    .out(_$_U17_out)
);
mantle_wire__typeBit2 _$_U18 (
    .in(I1_0_1),
    .out(_$_U18_out)
);
mantle_wire__typeBit2 _$_U19 (
    .in(I1_0_2),
    .out(_$_U19_out)
);
mantle_wire__typeBit2 _$_U20 (
    .in(I1_1_0),
    .out(_$_U20_out)
);
mantle_wire__typeBit2 _$_U21 (
    .in(I1_1_1),
    .out(_$_U21_out)
);
mantle_wire__typeBit2 _$_U22 (
    .in(I1_1_2),
    .out(_$_U22_out)
);
mantle_wire__typeBit2 _$_U23 (
    .in(I2_0_0),
    .out(_$_U23_out)
);
mantle_wire__typeBit2 _$_U24 (
    .in(I2_0_1),
    .out(_$_U24_out)
);
mantle_wire__typeBit2 _$_U25 (
    .in(I2_0_2),
    .out(_$_U25_out)
);
mantle_wire__typeBit2 _$_U26 (
    .in(I2_1_0),
    .out(_$_U26_out)
);
mantle_wire__typeBit2 _$_U27 (
    .in(I2_1_1),
    .out(_$_U27_out)
);
mantle_wire__typeBit2 _$_U28 (
    .in(I2_1_2),
    .out(_$_U28_out)
);
mantle_wire__typeBit2 _$_U29 (
    .in(I3_0_0),
    .out(_$_U29_out)
);
mantle_wire__typeBit2 _$_U30 (
    .in(I3_0_1),
    .out(_$_U30_out)
);
mantle_wire__typeBit2 _$_U31 (
    .in(I3_0_2),
    .out(_$_U31_out)
);
mantle_wire__typeBit2 _$_U32 (
    .in(I3_1_0),
    .out(_$_U32_out)
);
mantle_wire__typeBit2 _$_U33 (
    .in(I3_1_1),
    .out(_$_U33_out)
);
mantle_wire__typeBit2 _$_U34 (
    .in(I3_1_2),
    .out(_$_U34_out)
);
mantle_wire__typeBitIn2 _$_U35 (
    .in(O_0_0),
    .out(_$_U9_out[1:0])
);
mantle_wire__typeBitIn2 _$_U36 (
    .in(O_0_1),
    .out(_$_U9_out[3:2])
);
mantle_wire__typeBitIn2 _$_U37 (
    .in(O_0_2),
    .out(_$_U9_out[5:4])
);
mantle_wire__typeBitIn2 _$_U38 (
    .in(O_1_0),
    .out(_$_U9_out[7:6])
);
mantle_wire__typeBitIn2 _$_U39 (
    .in(O_1_1),
    .out(_$_U9_out[9:8])
);
mantle_wire__typeBitIn2 _$_U40 (
    .in(O_1_2),
    .out(_$_U9_out[11:10])
);
mantle_wire__typeBitIn12 _$_U5 (
    .in(_$_U5_in),
    .out({_$_U16_out[1:0],_$_U15_out[1:0],_$_U14_out[1:0],_$_U13_out[1:0],_$_U12_out[1:0],_$_U11_out[1:0]})
);
mantle_wire__typeBitIn12 _$_U6 (
    .in(_$_U6_in),
    .out({_$_U22_out[1:0],_$_U21_out[1:0],_$_U20_out[1:0],_$_U19_out[1:0],_$_U18_out[1:0],_$_U17_out[1:0]})
);
mantle_wire__typeBitIn12 _$_U7 (
    .in(_$_U7_in),
    .out({_$_U28_out[1:0],_$_U27_out[1:0],_$_U26_out[1:0],_$_U25_out[1:0],_$_U24_out[1:0],_$_U23_out[1:0]})
);
mantle_wire__typeBitIn12 _$_U8 (
    .in(_$_U8_in),
    .out({_$_U34_out[1:0],_$_U33_out[1:0],_$_U32_out[1:0],_$_U31_out[1:0],_$_U30_out[1:0],_$_U29_out[1:0]})
);
mantle_wire__typeBit12 _$_U9 (
    .in(coreir_commonlib_mux4x12_inst0_out),
    .out(_$_U9_out)
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
    input [1:0] I_4_0,
    input [1:0] I_4_1,
    input [1:0] I_4_2,
    input [1:0] I_5_0,
    input [1:0] I_5_1,
    input [1:0] I_5_2,
    output [1:0] O_0_0,
    output [1:0] O_0_1,
    output [1:0] O_0_2,
    output [1:0] O_1_0,
    output [1:0] O_1_1,
    output [1:0] O_1_2,
    input [1:0] x
);
Mux4xArray2_Array3_Array2_OutBit Mux4xArray2_Array3_Array2_OutBit_inst0 (
    .I0_0_0(I_0_0),
    .I0_0_1(I_0_1),
    .I0_0_2(I_0_2),
    .I0_1_0(I_1_0),
    .I0_1_1(I_1_1),
    .I0_1_2(I_1_2),
    .I1_0_0(I_1_0),
    .I1_0_1(I_1_1),
    .I1_0_2(I_1_2),
    .I1_1_0(I_2_0),
    .I1_1_1(I_2_1),
    .I1_1_2(I_2_2),
    .I2_0_0(I_2_0),
    .I2_0_1(I_2_1),
    .I2_0_2(I_2_2),
    .I2_1_0(I_3_0),
    .I2_1_1(I_3_1),
    .I2_1_2(I_3_2),
    .I3_0_0(I_3_0),
    .I3_0_1(I_3_1),
    .I3_0_2(I_3_2),
    .I3_1_0(I_4_0),
    .I3_1_1(I_4_1),
    .I3_1_2(I_4_2),
    .O_0_0(O_0_0),
    .O_0_1(O_0_1),
    .O_0_2(O_0_2),
    .O_1_0(O_1_0),
    .O_1_1(O_1_1),
    .O_1_2(O_1_2),
    .S(x)
);
endmodule

