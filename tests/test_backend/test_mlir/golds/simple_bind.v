module simple_bind_asserts(	// <stdin>:1:1
  input I, O, CLK);

  wire _magma_inline_wire0;	// <stdin>:2:10
  wire _magma_inline_wire1;	// <stdin>:5:10

  assign _magma_inline_wire0 = O;	// <stdin>:3:5
  assign _magma_inline_wire1 = I;	// <stdin>:6:5
  assert property (@(posedge CLK) _magma_inline_wire1 |-> ##1 _magma_inline_wire0);	// <stdin>:4:10, :7:10, :8:5
endmodule

module simple_bind(	// <stdin>:10:1
  input  I, CLK,
  output O);

  reg Register_inst0;	// <stdin>:11:10

  always_ff @(posedge CLK)	// <stdin>:12:5
    Register_inst0 <= I;	// <stdin>:13:9
  initial	// <stdin>:16:5
    Register_inst0 = 1'h0;	// <stdin>:15:10, :17:9
  /* This instance is elsewhere emitted as a bind statement.
    simple_bind_asserts simple_bind_asserts_inst (	// <stdin>:20:5
      .I   (I),
      .O   (Register_inst0),	// <stdin>:19:10
      .CLK (CLK)
    );
  */
  assign O = Register_inst0;	// <stdin>:19:10, :21:5
endmodule


// ----- 8< ----- FILE "bindfile" ----- 8< -----

bind simple_bind simple_bind_asserts simple_bind_asserts_inst (
  .I   (I),
  .O   (Register_inst0),
  .CLK (CLK)
);
