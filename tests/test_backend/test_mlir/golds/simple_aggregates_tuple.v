module simple_aggregates_product(	// <stdin>:1:1
  input  struct packed {logic [7:0] x; logic [7:0] y; } a,
  output struct packed {logic [7:0] x; logic [7:0] y; } y);

  assign y = '{x: (~a.x), y: (~a.y)};	// <stdin>:2:10, :4:10, :5:10, :6:10, :7:10, :8:5
endmodule

