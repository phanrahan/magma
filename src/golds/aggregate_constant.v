module aggregate_constant(	// <stdin>:1:1
  output struct packed {logic [7:0] x; logic [3:0] y; } y);

  assign y = '{x: (8'h0), y: (4'h0)};	// <stdin>:2:10, :3:10, :4:10, :5:5
endmodule

