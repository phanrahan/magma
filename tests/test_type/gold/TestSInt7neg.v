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
wire [6:0] magma_Bits_7_neg_inst0_in;
wire [6:0] magma_Bits_7_neg_inst0_out;
assign magma_Bits_7_neg_inst0_in = I;
coreir_neg #(
    .width(7)
) magma_Bits_7_neg_inst0 (
    .in(magma_Bits_7_neg_inst0_in),
    .out(magma_Bits_7_neg_inst0_out)
);
assign O = magma_Bits_7_neg_inst0_out;
endmodule

