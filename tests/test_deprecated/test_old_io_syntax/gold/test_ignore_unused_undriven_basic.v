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
wire corebit_term_inst0_in;
assign corebit_term_inst0_in = ~ (I ^ 1'b1);
corebit_term corebit_term_inst0 (
    .in(corebit_term_inst0_in)
);
corebit_undriven corebit_undriven_inst0 (
    .out(O)
);
endmodule

