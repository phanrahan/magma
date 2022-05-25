module complex_undriven(	// <stdin>:1:1
  output struct packed {logic [7:0] x; logic y; } O);

  wire [7:0] _T;	// <stdin>:2:10
  wire       _T_0;	// <stdin>:4:10

  assign O = '{x: _T, y: _T_0};	// <stdin>:3:10, :5:10, :6:10, :7:5
endmodule

