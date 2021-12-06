module mantle_concatNArrT__Ns88__t_childBitIn (
    input [7:0] in0,
    input [7:0] in1,
    output [15:0] out
);
assign out = {in1[7],in1[6],in1[5],in1[4],in1[3],in1[2],in1[1],in1[0],in0[7],in0[6],in0[5],in0[4],in0[3],in0[2],in0[1],in0[0]};
endmodule

module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module _Test (
    input [7:0] I0,
    output [3:0] O1,
    output [15:0] O2
);
wire [15:0] ConcatN_inst0_out;
wire [7:0] magma_UInt_8_not_inst0_out;
mantle_concatNArrT__Ns88__t_childBitIn ConcatN_inst0 (
    .in0(I0),
    .in1(8'h00),
    .out(ConcatN_inst0_out)
);
assign magma_UInt_8_not_inst0_out = ~ I0;
coreir_term #(
    .width(8)
) term_inst0 (
    .in(8'h00)
);
assign O1 = magma_UInt_8_not_inst0_out[3:0];
assign O2 = ~ ConcatN_inst0_out;
endmodule

