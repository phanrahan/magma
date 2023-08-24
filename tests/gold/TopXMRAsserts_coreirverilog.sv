module corebit_term (
    input in
);

endmodule

module TopXMRAsserts_coreirverilog (
    input I,
    input O,
    input other
);
corebit_term corebit_term_inst0 (
    .in(I)
);
corebit_term corebit_term_inst1 (
    .in(O)
);
corebit_term corebit_term_inst2 (
    .in(other)
);
endmodule


bind Top TopXMRAsserts_coreirverilog TopXMRAsserts_coreirverilog_inst (
    .I(I),
    .O(O),
    .other(middle._magma_bind_wire_0)
);