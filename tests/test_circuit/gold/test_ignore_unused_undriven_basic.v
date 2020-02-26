module corebit_undriven (
    output out
);

endmodule

module Main (
    input I,
    output O
);
corebit_undriven corebit_undriven_inst0 (
    .out(O)
);
endmodule

