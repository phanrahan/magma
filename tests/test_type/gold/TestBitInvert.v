module corebit_not (
    input in,
    output out
);
  assign out = ~in;
endmodule

module TestInvert (
    input I,
    output O
);
wire magma_Bit_not_inst0_in;
wire magma_Bit_not_inst0_out;
assign magma_Bit_not_inst0_in = I;
corebit_not magma_Bit_not_inst0 (
    .in(magma_Bit_not_inst0_in),
    .out(magma_Bit_not_inst0_out)
);
assign O = magma_Bit_not_inst0_out;
endmodule

