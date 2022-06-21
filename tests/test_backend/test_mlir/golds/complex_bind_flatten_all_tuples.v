module complex_bind_child(	// <stdin>:1:1
  input  I_I, CLK,
  output O_I);

  reg my_reg;	// <stdin>:2:10

  always_ff @(posedge CLK)	// <stdin>:3:5
    my_reg <= I_I;	// <stdin>:4:9
  initial	// <stdin>:7:5
    my_reg = 1'h0;	// <stdin>:6:10, :8:9
  assign O_I = I_I;	// <stdin>:11:5
endmodule

module complex_bind_asserts(	// <stdin>:13:1
  input I_I, O, CLK, I0, I1, I2, I3);

  wire _magma_inline_wire0;	// <stdin>:14:10
  wire _magma_inline_wire1;	// <stdin>:17:10
  wire _magma_inline_wire2;	// <stdin>:20:10

  assign _magma_inline_wire0 = O;	// <stdin>:15:5
  assign _magma_inline_wire1 = I_I;	// <stdin>:18:5
  assign _magma_inline_wire2 = I0;	// <stdin>:21:5
  assert property (@(posedge CLK) _magma_inline_wire1 |-> ##1 _magma_inline_wire0);assert property (_magma_inline_wire1 |-> _magma_inline_wire2;	// <stdin>:16:10, :19:10, :22:10, :23:5
endmodule

module complex_bind(	// <stdin>:25:1
  input  I_I, CLK,
  output O);

  wire complex_bind_asserts_inst_I0;	// <stdin>:45:5
  wire complex_bind_asserts_inst_I1;	// <stdin>:45:5
  wire complex_bind_asserts_inst_I2;	// <stdin>:45:5
  wire complex_bind_asserts_inst_I3;	// <stdin>:45:5
  wire complex_bind_child_inst0_O_I;	// <stdin>:38:10
  reg  Register_inst0;	// <stdin>:29:10

  always_ff @(posedge CLK)	// <stdin>:30:5
    Register_inst0 <= I_I;	// <stdin>:31:9
  initial	// <stdin>:34:5
    Register_inst0 = 1'h0;	// <stdin>:33:10, :35:9
  complex_bind_child complex_bind_child_inst0 (	// <stdin>:38:10
    .I_I (I_I),
    .CLK (CLK),
    .O_I (complex_bind_child_inst0_O_I)
  );
  assign complex_bind_asserts_inst_I0 = ~I_I;	// <stdin>:27:10, :45:5
  assign complex_bind_asserts_inst_I1 = I_I;	// <stdin>:39:10, :40:10, :45:5
  assign complex_bind_asserts_inst_I2 = complex_bind_child_inst0.O_I;	// <stdin>:41:10, :42:11, :45:5
  assign complex_bind_asserts_inst_I3 = complex_bind_child_inst0.my_reg.my_reg_O_I;	// <stdin>:43:11, :44:11, :45:5
  /* This instance is elsewhere emitted as a bind statement.
    complex_bind_asserts complex_bind_asserts_inst (	// <stdin>:45:5
      .I_I (I_I),
      .O   (Register_inst0),	// <stdin>:37:10
      .CLK (CLK),
      .I0  (complex_bind_asserts_inst_I0),	// <stdin>:45:5
      .I1  (complex_bind_asserts_inst_I1),	// <stdin>:45:5
      .I2  (complex_bind_asserts_inst_I2),	// <stdin>:45:5
      .I3  (complex_bind_asserts_inst_I3)	// <stdin>:45:5
    );
  */
  assign O = Register_inst0;	// <stdin>:37:10, :46:5
endmodule


// ----- 8< ----- FILE "bindfile" ----- 8< -----

bind complex_bind complex_bind_asserts complex_bind_asserts_inst (
  .I_I (I_I),
  .O   (Register_inst0),
  .CLK (CLK),
  .I0  (complex_bind_asserts_inst_I0),
  .I1  (complex_bind_asserts_inst_I1),
  .I2  (complex_bind_asserts_inst_I2),
  .I3  (complex_bind_asserts_inst_I3)
);
