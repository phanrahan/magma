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

module Mux2xArray3_Array2_OutBit (
    input [1:0] I0_0,
    input [1:0] I0_1,
    input [1:0] I0_2,
    input [1:0] I1_0,
    input [1:0] I1_1,
    input [1:0] I1_2,
    output [1:0] O_0,
    output [1:0] O_1,
    output [1:0] O_2,
    input S
);
wire [1:0] _$_U10_out;
wire [1:0] _$_U11_out;
wire [5:0] _$_U2_in;
wire [5:0] _$_U3_in;
wire [5:0] _$_U4_out;
wire [1:0] _$_U6_out;
wire [1:0] _$_U7_out;
wire [1:0] _$_U8_out;
wire [1:0] _$_U9_out;
reg [5:0] coreir_commonlib_mux2x6_inst0_out;
mantle_wire__typeBit2 _$_U10 (
    .in(I1_1),
    .out(_$_U10_out)
);
mantle_wire__typeBit2 _$_U11 (
    .in(I1_2),
    .out(_$_U11_out)
);
mantle_wire__typeBitIn2 _$_U12 (
    .in(O_0),
    .out(_$_U4_out[1:0])
);
mantle_wire__typeBitIn2 _$_U13 (
    .in(O_1),
    .out(_$_U4_out[3:2])
);
mantle_wire__typeBitIn2 _$_U14 (
    .in(O_2),
    .out(_$_U4_out[5:4])
);
mantle_wire__typeBitIn6 _$_U2 (
    .in(_$_U2_in),
    .out({_$_U8_out[1:0],_$_U7_out[1:0],_$_U6_out[1:0]})
);
mantle_wire__typeBitIn6 _$_U3 (
    .in(_$_U3_in),
    .out({_$_U11_out[1:0],_$_U10_out[1:0],_$_U9_out[1:0]})
);
mantle_wire__typeBit6 _$_U4 (
    .in(coreir_commonlib_mux2x6_inst0_out),
    .out(_$_U4_out)
);
mantle_wire__typeBit2 _$_U6 (
    .in(I0_0),
    .out(_$_U6_out)
);
mantle_wire__typeBit2 _$_U7 (
    .in(I0_1),
    .out(_$_U7_out)
);
mantle_wire__typeBit2 _$_U8 (
    .in(I0_2),
    .out(_$_U8_out)
);
mantle_wire__typeBit2 _$_U9 (
    .in(I1_0),
    .out(_$_U9_out)
);
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x6_inst0_out = _$_U2_in;
end else begin
    coreir_commonlib_mux2x6_inst0_out = _$_U3_in;
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
    output [1:0] O_3_2,
    output [1:0] O_4_0,
    output [1:0] O_4_1,
    output [1:0] O_4_2,
    output [1:0] O_5_0,
    output [1:0] O_5_1,
    output [1:0] O_5_2,
    input [1:0] x
);
wire [1:0] Mux2xArray3_Array2_OutBit_inst0_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst0_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst0_O_2;
wire [1:0] Mux2xArray3_Array2_OutBit_inst10_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst10_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst10_O_2;
wire [1:0] Mux2xArray3_Array2_OutBit_inst2_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst2_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst2_O_2;
wire [1:0] Mux2xArray3_Array2_OutBit_inst4_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst4_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst4_O_2;
wire [1:0] Mux2xArray3_Array2_OutBit_inst6_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst6_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst6_O_2;
wire [1:0] Mux2xArray3_Array2_OutBit_inst8_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst8_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst8_O_2;
wire [1:0] _$_U28_out;
wire [2:0] magma_Bits_3_sub_inst0_out;
wire [2:0] magma_Bits_3_sub_inst10_out;
wire [2:0] magma_Bits_3_sub_inst2_out;
wire [2:0] magma_Bits_3_sub_inst4_out;
wire [2:0] magma_Bits_3_sub_inst6_out;
wire [2:0] magma_Bits_3_sub_inst8_out;
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst0 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst0_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst0_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst0_O_2),
    .S(magma_Bits_3_sub_inst0_out[0])
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst1 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst0_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst0_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst0_O_2),
    .O_0(O_0_0),
    .O_1(O_0_1),
    .O_2(O_0_2),
    .S(1'b1 & (({1'b0,_$_U28_out[1:0]}) <= 3'h0))
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst10 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst10_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst10_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst10_O_2),
    .S(magma_Bits_3_sub_inst10_out[0])
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst11 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst10_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst10_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst10_O_2),
    .O_0(O_5_0),
    .O_1(O_5_1),
    .O_2(O_5_2),
    .S(1'b1 & ((3'((3'(({1'b0,_$_U28_out[1:0]}) + 3'h2)) - 3'h1)) >= 3'h5))
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst2 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst2_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst2_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst2_O_2),
    .S(magma_Bits_3_sub_inst2_out[0])
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst3 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst2_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst2_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst2_O_2),
    .O_0(O_1_0),
    .O_1(O_1_1),
    .O_2(O_1_2),
    .S((1'b1 & (({1'b0,_$_U28_out[1:0]}) <= 3'h1)) & ((3'((3'(({1'b0,_$_U28_out[1:0]}) + 3'h2)) - 3'h1)) >= 3'h1))
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst4 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst4_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst4_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst4_O_2),
    .S(magma_Bits_3_sub_inst4_out[0])
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst5 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst4_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst4_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst4_O_2),
    .O_0(O_2_0),
    .O_1(O_2_1),
    .O_2(O_2_2),
    .S((1'b1 & (({1'b0,_$_U28_out[1:0]}) <= 3'h2)) & ((3'((3'(({1'b0,_$_U28_out[1:0]}) + 3'h2)) - 3'h1)) >= 3'h2))
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst6 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst6_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst6_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst6_O_2),
    .S(magma_Bits_3_sub_inst6_out[0])
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst7 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst6_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst6_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst6_O_2),
    .O_0(O_3_0),
    .O_1(O_3_1),
    .O_2(O_3_2),
    .S(1'b1 & ((3'((3'(({1'b0,_$_U28_out[1:0]}) + 3'h2)) - 3'h1)) >= 3'h3))
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst8 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst8_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst8_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst8_O_2),
    .S(magma_Bits_3_sub_inst8_out[0])
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst9 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst8_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst8_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst8_O_2),
    .O_0(O_4_0),
    .O_1(O_4_1),
    .O_2(O_4_2),
    .S(1'b1 & ((3'((3'(({1'b0,_$_U28_out[1:0]}) + 3'h2)) - 3'h1)) >= 3'h4))
);
mantle_wire__typeBit2 _$_U28 (
    .in(x),
    .out(_$_U28_out)
);
assign magma_Bits_3_sub_inst0_out = 3'(3'h0 - ({1'b0,_$_U28_out[1:0]}));
assign magma_Bits_3_sub_inst10_out = 3'(3'h5 - ({1'b0,_$_U28_out[1:0]}));
assign magma_Bits_3_sub_inst2_out = 3'(3'h1 - ({1'b0,_$_U28_out[1:0]}));
assign magma_Bits_3_sub_inst4_out = 3'(3'h2 - ({1'b0,_$_U28_out[1:0]}));
assign magma_Bits_3_sub_inst6_out = 3'(3'h3 - ({1'b0,_$_U28_out[1:0]}));
assign magma_Bits_3_sub_inst8_out = 3'(3'h4 - ({1'b0,_$_U28_out[1:0]}));
endmodule

