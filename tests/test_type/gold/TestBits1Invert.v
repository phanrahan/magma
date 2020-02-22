module coreir_not #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = ~in;
endmodule

module TestInvert (
    input [0:0] I,
    output [0:0] O
);
wire [0:0] magma_Bits_1_not_inst0_out;
coreir_not #(
    .width(1)
) magma_Bits_1_not_inst0 (
    .in(I),
    .out(magma_Bits_1_not_inst0_out)
);
assign O = magma_Bits_1_not_inst0_out;
endmodule

