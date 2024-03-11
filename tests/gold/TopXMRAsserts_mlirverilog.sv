module TopXMRAsserts_mlirverilog(
  input I,
        O,
        other
);

endmodule


bind Top TopXMRAsserts_mlirverilog TopXMRAsserts_mlirverilog_inst (
    .I(I),
    .O(O),
    .other(middle._magma_bind_wire_0)
);