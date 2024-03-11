module TopBasicAsserts_mlirverilog(
  input I,
        O,
        other
);

endmodule


bind Top TopBasicAsserts_mlirverilog TopBasicAsserts_mlirverilog_inst (
    .I(I),
    .O(O),
    .other(_magma_bind_wire_0)
);