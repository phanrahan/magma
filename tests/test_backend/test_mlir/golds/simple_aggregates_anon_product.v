// Generated by CIRCT circtorg-0.0.0-1773-g7abbc4313
module simple_aggregates_anon_product(
  input  struct packed {logic [7:0] x; logic [7:0] y; } a,
  output struct packed {logic [7:0] x; logic [7:0] y; } y
);

  assign y = '{x: (~a.x), y: (~a.y)};
endmodule

