module complex_bind_asserts(	// <stdin>:1:1
  input I_I, O, CLK, I0);

  wire _magma_inline_wire0;	// <stdin>:2:10
  wire _magma_inline_wire1;	// <stdin>:5:10
  wire _magma_inline_wire2;	// <stdin>:8:10

  assign _magma_inline_wire0 = O;	// <stdin>:3:5
  assign _magma_inline_wire1 = I_I;	// <stdin>:6:5
  assign _magma_inline_wire2 = I0;	// <stdin>:9:5
  assert property (@(posedge CLK) _magma_inline_wire1 |-> ##1 _magma_inline_wire0);assert property (_magma_inline_wire1 |-> _magma_inline_wire2;	// <stdin>:4:10, :7:10, :10:10, :11:5
endmodule

module complex_bind(	// <stdin>:13:1
  input  I_I, CLK,
  output O);

  wire complex_bind_asserts_inst_I0;	// <stdin>:26:5
  reg  Register_inst0;	// <stdin>:17:10

  always_ff @(posedge CLK)	// <stdin>:18:5
    Register_inst0 <= I_I;	// <stdin>:19:9
  initial	// <stdin>:22:5
    Register_inst0 = 1'h0;	// <stdin>:21:10, :23:9
  assign complex_bind_asserts_inst_I0 = ~I_I;	// <stdin>:15:10, :26:5
  /* This instance is elsewhere emitted as a bind statement.
    complex_bind_asserts complex_bind_asserts_inst (	// <stdin>:26:5
      .I_I (I_I),
      .O   (Register_inst0),	// <stdin>:25:10
      .CLK (CLK),
      .I0  (complex_bind_asserts_inst_I0)	// <stdin>:26:5
    );
  */
  assign O = Register_inst0;	// <stdin>:25:10, :27:5
endmodule


// ----- 8< ----- FILE "bindfile" ----- 8< -----

bind complex_bind complex_bind_asserts complex_bind_asserts_inst (
  .I_I (I_I),
  .O   (Register_inst0),
  .CLK (CLK),
  .I0  (complex_bind_asserts_inst_I0)
);
