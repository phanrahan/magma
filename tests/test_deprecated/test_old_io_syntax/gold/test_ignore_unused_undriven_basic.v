module corebit_undriven (
    output out
);

endmodule

module corebit_term (
    input in
);

endmodule

module Main (
    input I,
    output O
);
wire magma_Bit_not_inst0_out;
corebit_term corebit_term_inst0 (
    .in(magma_Bit_not_inst0_out)
);
corebit_undriven corebit_undriven_inst0 (
    .out(O)
);
assign magma_Bit_not_inst0_out = ~ (I ^ 1'b1);
endmodule

