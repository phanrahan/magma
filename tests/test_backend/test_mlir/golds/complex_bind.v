module complex_bind_child(	// <stdin>:1:1
  input  struct packed {logic I; } I,
  input                            CLK,
  output struct packed {logic I; } O);

  struct packed {logic I; } my_reg;	// <stdin>:2:10

  always_ff @(posedge CLK)	// <stdin>:3:5
    my_reg <= I;	// <stdin>:4:9
  initial begin	// <stdin>:8:5
    automatic struct packed {logic I; } _T = '{I: (1'h0)};	// <stdin>:6:10, :7:10

    my_reg = _T;	// <stdin>:9:9
  end // initial
  assign O = I;	// <stdin>:12:5
endmodule

module complex_bind_asserts(	// <stdin>:14:1
  input struct packed {logic I; } I,
  input                           O, CLK, I0, I1, I2, I3);

  wire _magma_inline_wire0;	// <stdin>:15:10
  wire _magma_inline_wire1;	// <stdin>:19:10
  wire _magma_inline_wire2;	// <stdin>:22:10

  assign _magma_inline_wire0 = O;	// <stdin>:16:5
  assign _magma_inline_wire1 = I.I;	// <stdin>:18:10, :20:5
  assign _magma_inline_wire2 = I0;	// <stdin>:23:5
  assert property (@(posedge CLK) _magma_inline_wire1 |-> ##1 _magma_inline_wire0);assert property (_magma_inline_wire1 |-> _magma_inline_wire2;	// <stdin>:17:10, :21:10, :24:10, :25:5
endmodule

module complex_bind(	// <stdin>:27:1
  input  struct packed {logic I; } I,
  input                            CLK,
  output                           O);

  wire                           complex_bind_asserts_inst_I0;	// <stdin>:48:5
  wire                           complex_bind_asserts_inst_I1;	// <stdin>:48:5
  wire                           complex_bind_asserts_inst_I2;	// <stdin>:48:5
  wire                           complex_bind_asserts_inst_I3;	// <stdin>:48:5
  wire struct packed {logic I; } complex_bind_child_inst0_O;	// <stdin>:41:10
  reg                            Register_inst0;	// <stdin>:32:10

  wire _T = I.I;	// <stdin>:28:10
  always_ff @(posedge CLK)	// <stdin>:33:5
    Register_inst0 <= _T;	// <stdin>:34:9
  initial	// <stdin>:37:5
    Register_inst0 = 1'h0;	// <stdin>:36:10, :38:9
  complex_bind_child complex_bind_child_inst0 (	// <stdin>:41:10
    .I   (I),
    .CLK (CLK),
    .O   (complex_bind_child_inst0_O)
  );
  assign complex_bind_asserts_inst_I0 = ~_T;	// <stdin>:30:10, :48:5
  assign complex_bind_asserts_inst_I1 = I.I;	// <stdin>:42:10, :43:10, :48:5
  assign complex_bind_asserts_inst_I2 = complex_bind_child_inst0.O.I;	// <stdin>:44:11, :45:11, :48:5
  assign complex_bind_asserts_inst_I3 = complex_bind_child_inst0.my_reg.my_reg.O.I;	// <stdin>:46:11, :47:11, :48:5
  /* This instance is elsewhere emitted as a bind statement.
    complex_bind_asserts complex_bind_asserts_inst (	// <stdin>:48:5
      .I   (I),
      .O   (Register_inst0),	// <stdin>:40:10
      .CLK (CLK),
      .I0  (complex_bind_asserts_inst_I0),	// <stdin>:48:5
      .I1  (complex_bind_asserts_inst_I1),	// <stdin>:48:5
      .I2  (complex_bind_asserts_inst_I2),	// <stdin>:48:5
      .I3  (complex_bind_asserts_inst_I3)	// <stdin>:48:5
    );
  */
  assign O = Register_inst0;	// <stdin>:40:10, :49:5
endmodule


// ----- 8< ----- FILE "bindfile" ----- 8< -----

bind complex_bind complex_bind_asserts complex_bind_asserts_inst (
  .I   (I),
  .O   (Register_inst0),
  .CLK (CLK),
  .I0  (complex_bind_asserts_inst_I0),
  .I1  (complex_bind_asserts_inst_I1),
  .I2  (complex_bind_asserts_inst_I2),
  .I3  (complex_bind_asserts_inst_I3)
);
