module coreir_neg #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = -in;
endmodule

module TestNegate (
    input [6:0] I,
    output [6:0] O
);
wire [6:0] magma_SInt_7_neg_inst0_out;
coreir_neg #(
    .width(7)
) magma_SInt_7_neg_inst0 (
    .in(I),
    .out(magma_SInt_7_neg_inst0_out)
);
assign O = magma_SInt_7_neg_inst0_out;
endmodule

