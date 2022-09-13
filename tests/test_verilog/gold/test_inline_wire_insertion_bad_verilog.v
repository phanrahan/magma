module test_wire_insertion_bad_verilog(	// <stdin>:1:1
  input  [31:0] I,
  output        O);

  wire _magma_inline_wire0;	// <stdin>:5:10

  wire _I_0 = I[0];	// <stdin>:2:10
  `ifdef LOGGING_ON	// <stdin>:4:5
  assign _magma_inline_wire0 = _I_0;	// <stdin>:6:5
  $display("%x", _magma_inline_wire0);	// <stdin>:7:10, :8:5
  `endif LOGGING_ON	// <stdin>:10:5
  assign O = _I_0;	// <stdin>:11:5
endmodule

