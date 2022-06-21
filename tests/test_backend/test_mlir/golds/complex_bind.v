module complex_bind_child(	// <stdin>:1:1
  input  struct packed {logic I; } I,
  output struct packed {logic I; } O);

  assign O = I;	// <stdin>:2:5
endmodule

module complex_bind_asserts(	// <stdin>:4:1
  input struct packed {logic I; } I,
  input                           O, CLK, I0, I1, I2);

  wire _magma_inline_wire0;	// <stdin>:5:10
  wire _magma_inline_wire1;	// <stdin>:9:10
  wire _magma_inline_wire2;	// <stdin>:12:10

  assign _magma_inline_wire0 = O;	// <stdin>:6:5
  assign _magma_inline_wire1 = I.I;	// <stdin>:8:10, :10:5
  assign _magma_inline_wire2 = I0;	// <stdin>:13:5
  assert property (@(posedge CLK) _magma_inline_wire1 |-> ##1 _magma_inline_wire0);assert property (_magma_inline_wire1 |-> _magma_inline_wire2;	// <stdin>:7:10, :11:10, :14:10, :15:5
endmodule

module complex_bind(	// <stdin>:17:1
  input  struct packed {logic I; } I,
  input                            CLK,
  output                           O);

  wire                           complex_bind_asserts_inst_I0;	// <stdin>:36:5
  wire                           complex_bind_asserts_inst_I1;	// <stdin>:36:5
  wire                           complex_bind_asserts_inst_I2;	// <stdin>:36:5
  wire struct packed {logic I; } complex_bind_child_inst0_O;	// <stdin>:31:10
  reg                            Register_inst0;	// <stdin>:22:10

  wire _T = I.I;	// <stdin>:18:10
  always_ff @(posedge CLK)	// <stdin>:23:5
    Register_inst0 <= _T;	// <stdin>:24:9
  initial	// <stdin>:27:5
    Register_inst0 = 1'h0;	// <stdin>:26:10, :28:9
  complex_bind_child complex_bind_child_inst0 (	// <stdin>:31:10
    .I (I),
    .O (complex_bind_child_inst0_O)
  );
  assign complex_bind_asserts_inst_I0 = ~_T;	// <stdin>:20:10, :36:5
  assign complex_bind_asserts_inst_I1 = I.I;	// <stdin>:32:10, :33:10, :36:5
  assign complex_bind_asserts_inst_I2 = complex_bind_child_inst0.O.I;	// <stdin>:34:11, :35:11, :36:5
  /* This instance is elsewhere emitted as a bind statement.
    complex_bind_asserts complex_bind_asserts_inst (	// <stdin>:36:5
      .I   (I),
      .O   (Register_inst0),	// <stdin>:30:10
      .CLK (CLK),
      .I0  (complex_bind_asserts_inst_I0),	// <stdin>:36:5
      .I1  (complex_bind_asserts_inst_I1),	// <stdin>:36:5
      .I2  (complex_bind_asserts_inst_I2)	// <stdin>:36:5
    );
  */
  assign O = Register_inst0;	// <stdin>:30:10, :37:5
endmodule


// ----- 8< ----- FILE "bindfile" ----- 8< -----

bind complex_bind complex_bind_asserts complex_bind_asserts_inst (
  .I   (I),
  .O   (Register_inst0),
  .CLK (CLK),
  .I0  (complex_bind_asserts_inst_I0),
  .I1  (complex_bind_asserts_inst_I1),
  .I2  (complex_bind_asserts_inst_I2)
);
