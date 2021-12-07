module mantle_concatNArrT__Ns115__t_childBitIn (
    input [0:0] in0,
    input [14:0] in1,
    output [15:0] out
);
assign out = {in1[14],in1[13],in1[12],in1[11],in1[10],in1[9],in1[8],in1[7],in1[6],in1[5],in1[4],in1[3],in1[2],in1[1],in1[0],in0[0]};
endmodule

module _Test (
    input [7:0] I0,
    output [0:0] O1,
    output [15:0] O2
);
wire coreir_andr_8_inst1_out;
mantle_concatNArrT__Ns115__t_childBitIn ConcatN_inst0 (
    .in0(coreir_andr_8_inst1_out),
    .in1(15'h0000),
    .out(O2)
);
assign coreir_andr_8_inst1_out = & I0;
assign O1 = & I0;
endmodule

