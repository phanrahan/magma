module coreir_neg #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = -in;
endmodule

module TestNegate (
    input [2:0] I,
    output [2:0] O
);
wire [2:0] magma_SInt_3_neg_inst0_out;
coreir_neg #(
    .width(3)
) magma_SInt_3_neg_inst0 (
    .in(I),
    .out(magma_SInt_3_neg_inst0_out)
);
assign O = magma_SInt_3_neg_inst0_out;
endmodule

