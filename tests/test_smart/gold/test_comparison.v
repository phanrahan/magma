module mantle_concatNArrT__Ns84__t_childBitIn (
    input [7:0] in0,
    input [3:0] in1,
    output [11:0] out
);
assign out = {in1[3],in1[2],in1[1],in1[0],in0[7],in0[6],in0[5],in0[4],in0[3],in0[2],in0[1],in0[0]};
endmodule

module mantle_concatNArrT__Ns115__t_childBitIn (
    input [0:0] in0,
    input [14:0] in1,
    output [15:0] out
);
assign out = {in1[14],in1[13],in1[12],in1[11],in1[10],in1[9],in1[8],in1[7],in1[6],in1[5],in1[4],in1[3],in1[2],in1[1],in1[0],in0[0]};
endmodule

module _Test (
    input [7:0] I0,
    input [11:0] I1,
    output [0:0] O1,
    output [15:0] O2
);
wire [11:0] ConcatN_inst0_out;
wire [11:0] ConcatN_inst1_out;
wire magma_UInt_12_eq_inst1_out;
mantle_concatNArrT__Ns84__t_childBitIn ConcatN_inst0 (
    .in0(I0),
    .in1(4'h0),
    .out(ConcatN_inst0_out)
);
mantle_concatNArrT__Ns84__t_childBitIn ConcatN_inst1 (
    .in0(I0),
    .in1(4'h0),
    .out(ConcatN_inst1_out)
);
mantle_concatNArrT__Ns115__t_childBitIn ConcatN_inst2 (
    .in0(magma_UInt_12_eq_inst1_out),
    .in1(15'h0000),
    .out(O2)
);
assign magma_UInt_12_eq_inst1_out = ConcatN_inst1_out == I1;
assign O1 = ConcatN_inst0_out == I1;
endmodule

