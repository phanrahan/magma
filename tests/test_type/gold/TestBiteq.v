module corebit_xor (
    input in0,
    input in1,
    output out
);
  assign out = in0 ^ in1;
endmodule

module corebit_not (
    input in,
    output out
);
  assign out = ~in;
endmodule

module TestBinary (
    input I0,
    input I1,
    output O
);
wire magma_Bit_not_inst0_out;
wire magma_Bit_xor_inst0_out;
corebit_not magma_Bit_not_inst0 (
    .in(magma_Bit_xor_inst0_out),
    .out(magma_Bit_not_inst0_out)
);
corebit_xor magma_Bit_xor_inst0 (
    .in0(I0),
    .in1(I1),
    .out(magma_Bit_xor_inst0_out)
);
assign O = magma_Bit_not_inst0_out;
endmodule

