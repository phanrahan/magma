module complex_undriven(	// <stdin>:1:1
  output struct packed {logic [7:0] x; logic y; } O);

  assign O = '{x: (8'bx), y: (1'bx)};	// <stdin>:2:10, :4:10, :6:10, :7:5
endmodule

