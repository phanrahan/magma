module COND1_compile_guard(
  input port_0,
        port_1
);

  reg Register_inst0;
  always_ff @(posedge port_1)
    Register_inst0 <= port_0;
  initial
    Register_inst0 = 1'h0;
endmodule

module COND2_compile_guard(
  input port_0,
        port_1
);

  reg Register_inst0;
  always_ff @(posedge port_1)
    Register_inst0 <= port_0;
  initial
    Register_inst0 = 1'h0;
endmodule

module simple_compile_guard(
  input  I,
         CLK,
  output O
);

  reg _GEN;
  `ifdef COND1
    assign _GEN = I;
    COND1_compile_guard COND1_compile_guard (
      .port_0 (I),
      .port_1 (CLK)
    );
  `else  // COND1
    `ifdef COND2
      assign _GEN = ~I;
    `else  // COND2
      assign _GEN = 1'h0;
    `endif // COND2
  `endif // COND1
  `ifndef COND2
    COND2_compile_guard COND2_compile_guard (
      .port_0 (I),
      .port_1 (CLK)
    );
  `endif // not def COND2
  assign O = _GEN;
endmodule

