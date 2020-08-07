module coreir_not #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = ~in;
endmodule

module TestInvert (
    input [2:0] I,
    output [2:0] O
);
wire [2:0] magma_Bits_3_not_inst0_in;
wire [2:0] magma_Bits_3_not_inst0_out;
assign magma_Bits_3_not_inst0_in = I;
coreir_not #(
    .width(3)
) magma_Bits_3_not_inst0 (
    .in(magma_Bits_3_not_inst0_in),
    .out(magma_Bits_3_not_inst0_out)
);
assign O = magma_Bits_3_not_inst0_out;
endmodule

