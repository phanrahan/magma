module simple_aggregates_tuple(
  input  struct packed {logic [7:0] x; logic [7:0] y; } a,
  output struct packed {logic [7:0] x; logic [7:0] y; } y);

  wire struct packed {logic [7:0] x; logic [7:0] y; } _T = '{x: (~a.x), y: (~a.y)};	// <stdin>:4:10, :5:10, :6:10, :7:10, :8:10
  assign y = _T;	// <stdin>:9:5
endmodule

