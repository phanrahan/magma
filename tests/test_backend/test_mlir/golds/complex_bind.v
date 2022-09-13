module complex_bind_asserts(	// <stdin>:1:1
  input struct packed {logic I; } I,
  input                           O, CLK, I0);

  wire _magma_inline_wire0;	// <stdin>:2:10
  wire _magma_inline_wire1;	// <stdin>:6:10
  wire _magma_inline_wire2;	// <stdin>:9:10

  assign _magma_inline_wire0 = O;	// <stdin>:3:5
  assign _magma_inline_wire1 = I.I;	// <stdin>:5:10, :7:5
  assign _magma_inline_wire2 = I0;	// <stdin>:10:5
  assert property (@(posedge CLK) _magma_inline_wire1 |-> ##1 _magma_inline_wire0);assert property (_magma_inline_wire1 |-> _magma_inline_wire2;	// <stdin>:4:10, :8:10, :11:10, :12:5
endmodule

module complex_bind(	// <stdin>:14:1
  input  struct packed {logic I; } I,
  input                            CLK,
  output                           O);

  wire complex_bind_asserts_inst_I0;	// <stdin>:28:5
  reg  Register_inst0;	// <stdin>:19:10

  wire _T = I.I;	// <stdin>:15:10
  always_ff @(posedge CLK)	// <stdin>:20:5
    Register_inst0 <= _T;	// <stdin>:21:9
  initial	// <stdin>:24:5
    Register_inst0 = 1'h0;	// <stdin>:23:10, :25:9
  assign complex_bind_asserts_inst_I0 = ~_T;	// <stdin>:17:10, :28:5
  /* This instance is elsewhere emitted as a bind statement.
    complex_bind_asserts complex_bind_asserts_inst (	// <stdin>:28:5
      .I   (I),
      .O   (Register_inst0),	// <stdin>:27:10
      .CLK (CLK),
      .I0  (complex_bind_asserts_inst_I0)	// <stdin>:28:5
    );
  */
  assign O = Register_inst0;	// <stdin>:27:10, :29:5
endmodule


// ----- 8< ----- FILE "bindfile" ----- 8< -----

bind complex_bind complex_bind_asserts complex_bind_asserts_inst (
  .I   (I),
  .O   (Register_inst0),
  .CLK (CLK),
  .I0  (complex_bind_asserts_inst_I0)
);
