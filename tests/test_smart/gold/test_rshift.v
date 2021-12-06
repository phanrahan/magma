module mantle_concatNArrT__Ns88__t_childBitIn (
    input [7:0] in0,
    input [7:0] in1,
    output [15:0] out
);
assign out = {in1[7],in1[6],in1[5],in1[4],in1[3],in1[2],in1[1],in1[0],in0[7],in0[6],in0[5],in0[4],in0[3],in0[2],in0[1],in0[0]};
endmodule

module mantle_concatNArrT__Ns44__t_childBitIn (
    input [3:0] in0,
    input [3:0] in1,
    output [7:0] out
);
assign out = {in1[3],in1[2],in1[1],in1[0],in0[3],in0[2],in0[1],in0[0]};
endmodule

module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module _Test (
    input [7:0] I0,
    input [3:0] I1,
    output [3:0] O1,
    output [7:0] O2,
    output [15:0] O3
);
wire [7:0] ConcatN_inst0_out;
wire [7:0] ConcatN_inst1_out;
wire [7:0] ConcatN_inst2_out;
wire [7:0] magma_UInt_8_lshr_inst0_out;
wire [7:0] magma_UInt_8_lshr_inst2_out;
mantle_concatNArrT__Ns44__t_childBitIn ConcatN_inst0 (
    .in0(I1),
    .in1(4'h0),
    .out(ConcatN_inst0_out)
);
mantle_concatNArrT__Ns44__t_childBitIn ConcatN_inst1 (
    .in0(I1),
    .in1(4'h0),
    .out(ConcatN_inst1_out)
);
mantle_concatNArrT__Ns44__t_childBitIn ConcatN_inst2 (
    .in0(I1),
    .in1(4'h0),
    .out(ConcatN_inst2_out)
);
mantle_concatNArrT__Ns88__t_childBitIn ConcatN_inst3 (
    .in0(magma_UInt_8_lshr_inst2_out),
    .in1(8'h00),
    .out(O3)
);
assign magma_UInt_8_lshr_inst0_out = I0 >> ConcatN_inst0_out;
assign magma_UInt_8_lshr_inst2_out = I0 >> ConcatN_inst2_out;
coreir_term #(
    .width(4)
) term_inst0 (
    .in(4'h0)
);
coreir_term #(
    .width(4)
) term_inst1 (
    .in(4'h0)
);
coreir_term #(
    .width(4)
) term_inst2 (
    .in(4'h0)
);
coreir_term #(
    .width(8)
) term_inst3 (
    .in(8'h00)
);
assign O1 = magma_UInt_8_lshr_inst0_out[3:0];
assign O2 = I0 >> ConcatN_inst1_out;
endmodule

