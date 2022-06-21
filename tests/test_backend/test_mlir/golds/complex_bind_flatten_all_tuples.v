module complex_bind_child(	// <stdin>:1:1
  input  I_I,
  output O_I);

  assign O_I = I_I;	// <stdin>:2:5
endmodule

module complex_bind_asserts(	// <stdin>:4:1
  input I_I, O, CLK, I0, I1, I2);

  wire _magma_inline_wire0;	// <stdin>:5:10
  wire _magma_inline_wire1;	// <stdin>:8:10
  wire _magma_inline_wire2;	// <stdin>:11:10

  assign _magma_inline_wire0 = O;	// <stdin>:6:5
  assign _magma_inline_wire1 = I_I;	// <stdin>:9:5
  assign _magma_inline_wire2 = I0;	// <stdin>:12:5
  assert property (@(posedge CLK) _magma_inline_wire1 |-> ##1 _magma_inline_wire0);assert property (_magma_inline_wire1 |-> _magma_inline_wire2;	// <stdin>:7:10, :10:10, :13:10, :14:5
endmodule

module complex_bind(	// <stdin>:16:1
  input  I_I, CLK,
  output O);

  wire complex_bind_asserts_inst_I0;	// <stdin>:34:5
  wire complex_bind_asserts_inst_I1;	// <stdin>:34:5
  wire complex_bind_asserts_inst_I2;	// <stdin>:34:5
  wire complex_bind_child_inst0_O_I;	// <stdin>:29:10
  reg  Register_inst0;	// <stdin>:20:10

  always_ff @(posedge CLK)	// <stdin>:21:5
    Register_inst0 <= I_I;	// <stdin>:22:9
  initial	// <stdin>:25:5
    Register_inst0 = 1'h0;	// <stdin>:24:10, :26:9
  complex_bind_child complex_bind_child_inst0 (	// <stdin>:29:10
    .I_I (I_I),
    .O_I (complex_bind_child_inst0_O_I)
  );
  assign complex_bind_asserts_inst_I0 = ~I_I;	// <stdin>:18:10, :34:5
  assign complex_bind_asserts_inst_I1 = I_I;	// <stdin>:30:10, :31:10, :34:5
  assign complex_bind_asserts_inst_I2 = complex_bind_child_inst0.O_I;	// <stdin>:32:10, :33:11, :34:5
  /* This instance is elsewhere emitted as a bind statement.
    complex_bind_asserts complex_bind_asserts_inst (	// <stdin>:34:5
      .I_I (I_I),
      .O   (Register_inst0),	// <stdin>:28:10
      .CLK (CLK),
      .I0  (complex_bind_asserts_inst_I0),	// <stdin>:34:5
      .I1  (complex_bind_asserts_inst_I1),	// <stdin>:34:5
      .I2  (complex_bind_asserts_inst_I2)	// <stdin>:34:5
    );
  */
  assign O = Register_inst0;	// <stdin>:28:10, :35:5
endmodule


// ----- 8< ----- FILE "bindfile" ----- 8< -----

bind complex_bind complex_bind_asserts complex_bind_asserts_inst (
  .I_I (I_I),
  .O   (Register_inst0),
  .CLK (CLK),
  .I0  (complex_bind_asserts_inst_I0),
  .I1  (complex_bind_asserts_inst_I1),
  .I2  (complex_bind_asserts_inst_I2)
);
