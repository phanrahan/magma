module aggregate_constant(
  output struct packed {logic [7:0] x; logic [3:0] y; } y
);

  assign y = '{x: 8'h0, y: 4'h0};
endmodule

