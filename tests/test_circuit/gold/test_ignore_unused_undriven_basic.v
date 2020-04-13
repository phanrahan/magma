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
corebit_term corebit_term_inst0 (
    .in(~ I)
);
corebit_undriven corebit_undriven_inst0 (
    .out(O)
);
endmodule

