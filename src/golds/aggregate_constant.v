module aggregate_constant(
  output struct packed {logic [7:0] x; logic [3:0] y; } y);

  wire struct packed {logic [7:0] x; logic [3:0] y; } _T = '{x: (8'h0), y: (4'h0)};	// <stdin>:3:14, :4:14, :5:10
  assign y = _T;	// <stdin>:6:5
endmodule

