// Generated by CIRCT circtorg-0.0.0-1773-g7abbc4313
module simple_aggregates_anon_product(
  input  [7:0] a_x,
               a_y,
  output [7:0] y_x,
               y_y
);

  assign y_x = ~a_x;
  assign y_y = ~a_y;
endmodule

