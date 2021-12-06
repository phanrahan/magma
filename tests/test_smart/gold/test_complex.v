module mantle_concatNArrT__Ns93__t_childBitIn (
    input [8:0] in0,
    input [2:0] in1,
    output [11:0] out
);
assign out = {in1[2],in1[1],in1[0],in0[8],in0[7],in0[6],in0[5],in0[4],in0[3],in0[2],in0[1],in0[0]};
endmodule

module mantle_concatNArrT__Ns75__t_childBitIn (
    input [6:0] in0,
    input [4:0] in1,
    output [11:0] out
);
assign out = {in1[4],in1[3],in1[2],in1[1],in1[0],in0[6],in0[5],in0[4],in0[3],in0[2],in0[1],in0[0]};
endmodule

module mantle_concatNArrT__Ns16__t_childBitIn (
    input [0:0] in0,
    input [5:0] in1,
    output [6:0] out
);
assign out = {in1[5],in1[4],in1[3],in1[2],in1[1],in1[0],in0[0]};
endmodule

module mantle_concatNArrT__Ns111__t_childBitIn (
    input [0:0] in0,
    input [10:0] in1,
    output [11:0] out
);
assign out = {in1[10],in1[9],in1[8],in1[7],in1[6],in1[5],in1[4],in1[3],in1[2],in1[1],in1[0],in0[0]};
endmodule

module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module _Test (
    input [6:0] I0,
    input [8:0] I1,
    input [11:0] I2,
    output [9:0] O,
    output [6:0] O2,
    output [0:0] O3
);
wire [11:0] ConcatN_inst0_out;
wire [11:0] ConcatN_inst1_out;
wire [11:0] ConcatN_inst2_out;
wire [11:0] ConcatN_inst3_out;
wire [6:0] ConcatN_inst4_out;
wire coreir_andr_7_inst0_out;
wire magma_SInt_12_sle_inst0_out;
wire [11:0] magma_UInt_12_shl_inst0_out;
mantle_concatNArrT__Ns75__t_childBitIn ConcatN_inst0 (
    .in0(I0),
    .in1(5'h00),
    .out(ConcatN_inst0_out)
);
mantle_concatNArrT__Ns93__t_childBitIn ConcatN_inst1 (
    .in0(I1),
    .in1(3'h0),
    .out(ConcatN_inst1_out)
);
mantle_concatNArrT__Ns111__t_childBitIn ConcatN_inst2 (
    .in0(coreir_andr_7_inst0_out),
    .in1(11'h000),
    .out(ConcatN_inst2_out)
);
wire [2:0] ConcatN_inst3_in1;
assign ConcatN_inst3_in1 = {I1[8],I1[8],I1[8]};
mantle_concatNArrT__Ns93__t_childBitIn ConcatN_inst3 (
    .in0(I1),
    .in1(ConcatN_inst3_in1),
    .out(ConcatN_inst3_out)
);
wire [5:0] ConcatN_inst4_in1;
assign ConcatN_inst4_in1 = {magma_SInt_12_sle_inst0_out,magma_SInt_12_sle_inst0_out,magma_SInt_12_sle_inst0_out,magma_SInt_12_sle_inst0_out,magma_SInt_12_sle_inst0_out,magma_SInt_12_sle_inst0_out};
mantle_concatNArrT__Ns16__t_childBitIn ConcatN_inst4 (
    .in0(magma_SInt_12_sle_inst0_out),
    .in1(ConcatN_inst4_in1),
    .out(ConcatN_inst4_out)
);
assign coreir_andr_7_inst0_out = & I0;
assign magma_SInt_12_sle_inst0_out = ($signed(ConcatN_inst3_out)) <= ($signed(I2));
assign magma_UInt_12_shl_inst0_out = (12'((~ (12'(ConcatN_inst0_out + ConcatN_inst1_out))) + I2)) << ConcatN_inst2_out;
coreir_term #(
    .width(5)
) term_inst0 (
    .in(5'h00)
);
coreir_term #(
    .width(3)
) term_inst1 (
    .in(3'h0)
);
coreir_term #(
    .width(11)
) term_inst2 (
    .in(11'h000)
);
assign O = magma_UInt_12_shl_inst0_out[9:0];
assign O2 = 7'(ConcatN_inst4_out + I0);
assign O3 = I0[0];
endmodule

