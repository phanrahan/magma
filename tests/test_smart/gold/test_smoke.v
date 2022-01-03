module mantle_concatNArrT__Ns275__t_childBitIn (
    input [26:0] in0,
    input [4:0] in1,
    output [31:0] out
);
assign out = {in1[4],in1[3],in1[2],in1[1],in1[0],in0[26],in0[25],in0[24],in0[23],in0[22],in0[21],in0[20],in0[19],in0[18],in0[17],in0[16],in0[15],in0[14],in0[13],in0[12],in0[11],in0[10],in0[9],in0[8],in0[7],in0[6],in0[5],in0[4],in0[3],in0[2],in0[1],in0[0]};
endmodule

module mantle_concatNArrT__Ns19__t_childBitIn (
    input [0:0] in0,
    input [8:0] in1,
    output [9:0] out
);
assign out = {in1[8],in1[7],in1[6],in1[5],in1[4],in1[3],in1[2],in1[1],in1[0],in0[0]};
endmodule

module mantle_concatNArrT__Ns13__t_childBitIn (
    input [0:0] in0,
    input [2:0] in1,
    output [3:0] out
);
assign out = {in1[2],in1[1],in1[0],in0[0]};
endmodule

module mantle_concatNArrT__Ns111__t_childBitIn (
    input [0:0] in0,
    input [10:0] in1,
    output [11:0] out
);
assign out = {in1[10],in1[9],in1[8],in1[7],in1[6],in1[5],in1[4],in1[3],in1[2],in1[1],in1[0],in0[0]};
endmodule

module mantle_concatNArrT__Ns106__t_childBitIn (
    input [9:0] in0,
    input [5:0] in1,
    output [15:0] out
);
assign out = {in1[5],in1[4],in1[3],in1[2],in1[1],in1[0],in0[9],in0[8],in0[7],in0[6],in0[5],in0[4],in0[3],in0[2],in0[1],in0[0]};
endmodule

module Test (
    output [9:0] port0,
    input [15:0] port1,
    output [15:0] port2,
    input [9:0] port3,
    output [9:0] port4,
    input [0:0] port5,
    output [0:0] port6,
    input [9:0] port7,
    output [11:0] port8,
    input [9:0] port9,
    input [15:0] port10,
    output [0:0] port11,
    input [9:0] port12,
    input [0:0] port13,
    output [15:0] port14,
    input [9:0] port15,
    output [11:0] port16,
    input [9:0] port17,
    input [15:0] port18,
    output [3:0] port19,
    input [9:0] port20,
    output [9:0] port21,
    input [9:0] port22,
    input [15:0] port23,
    output [15:0] port24,
    input [9:0] port25,
    input [15:0] port26,
    output [9:0] port27,
    input [9:0] port28,
    input [0:0] port29,
    output [0:0] port30,
    input [9:0] port31,
    input [0:0] port32,
    output [31:0] port33,
    input [9:0] port34,
    input [15:0] port35,
    input [0:0] port36
);
wire [9:0] ConcatN_inst10_out;
wire [9:0] ConcatN_inst11_out;
wire [15:0] ConcatN_inst2_out;
wire [9:0] ConcatN_inst3_out;
wire [15:0] ConcatN_inst4_out;
wire [15:0] ConcatN_inst5_out;
wire [15:0] ConcatN_inst8_out;
wire [15:0] ConcatN_inst9_out;
wire coreir_andr_10_inst0_out;
wire [9:0] magma_UInt_10_add_inst0_out;
wire [9:0] magma_UInt_10_shl_inst1_out;
wire [15:0] magma_UInt_16_add_inst0_out;
wire [15:0] magma_UInt_16_shl_inst0_out;
wire magma_UInt_16_ule_inst0_out;
mantle_concatNArrT__Ns106__t_childBitIn ConcatN_inst0 (
    .in0(port3),
    .in1(6'h00),
    .out(port2)
);
mantle_concatNArrT__Ns19__t_childBitIn ConcatN_inst1 (
    .in0(port5),
    .in1(9'h000),
    .out(port4)
);
mantle_concatNArrT__Ns19__t_childBitIn ConcatN_inst10 (
    .in0(port29),
    .in1(9'h000),
    .out(ConcatN_inst10_out)
);
mantle_concatNArrT__Ns19__t_childBitIn ConcatN_inst11 (
    .in0(port32),
    .in1(9'h000),
    .out(ConcatN_inst11_out)
);
wire [26:0] ConcatN_inst12_in0;
assign ConcatN_inst12_in0 = {port36[0],port35[15:0],port34[9:0]};
mantle_concatNArrT__Ns275__t_childBitIn ConcatN_inst12 (
    .in0(ConcatN_inst12_in0),
    .in1(5'h00),
    .out(port33)
);
mantle_concatNArrT__Ns106__t_childBitIn ConcatN_inst2 (
    .in0(port9),
    .in1(6'h00),
    .out(ConcatN_inst2_out)
);
mantle_concatNArrT__Ns19__t_childBitIn ConcatN_inst3 (
    .in0(port13),
    .in1(9'h000),
    .out(ConcatN_inst3_out)
);
mantle_concatNArrT__Ns106__t_childBitIn ConcatN_inst4 (
    .in0(port15),
    .in1(6'h00),
    .out(ConcatN_inst4_out)
);
mantle_concatNArrT__Ns106__t_childBitIn ConcatN_inst5 (
    .in0(port17),
    .in1(6'h00),
    .out(ConcatN_inst5_out)
);
mantle_concatNArrT__Ns111__t_childBitIn ConcatN_inst6 (
    .in0(magma_UInt_16_ule_inst0_out),
    .in1(11'h000),
    .out(port16)
);
mantle_concatNArrT__Ns13__t_childBitIn ConcatN_inst7 (
    .in0(coreir_andr_10_inst0_out),
    .in1(3'h0),
    .out(port19)
);
mantle_concatNArrT__Ns106__t_childBitIn ConcatN_inst8 (
    .in0(port22),
    .in1(6'h00),
    .out(ConcatN_inst8_out)
);
mantle_concatNArrT__Ns106__t_childBitIn ConcatN_inst9 (
    .in0(port25),
    .in1(6'h00),
    .out(ConcatN_inst9_out)
);
assign coreir_andr_10_inst0_out = & port20;
assign magma_UInt_10_add_inst0_out = 10'(port12 + ConcatN_inst3_out);
assign magma_UInt_10_shl_inst1_out = ConcatN_inst11_out << port31;
assign magma_UInt_16_add_inst0_out = 16'(ConcatN_inst2_out + port10);
assign magma_UInt_16_shl_inst0_out = ConcatN_inst8_out << port23;
assign magma_UInt_16_ule_inst0_out = ConcatN_inst5_out <= port18;
assign port0 = {port1[9],port1[8],port1[7],port1[6],port1[5],port1[4],port1[3],port1[2],port1[1],port1[0]};
assign port6 = port7[0];
assign port8 = magma_UInt_16_add_inst0_out[11:0];
assign port11 = magma_UInt_10_add_inst0_out[0:0];
assign port14 = ~ ConcatN_inst4_out;
assign port21 = magma_UInt_16_shl_inst0_out[9:0];
assign port24 = port26 << ConcatN_inst9_out;
assign port27 = port28 << ConcatN_inst10_out;
assign port30 = magma_UInt_10_shl_inst1_out[0:0];
endmodule

