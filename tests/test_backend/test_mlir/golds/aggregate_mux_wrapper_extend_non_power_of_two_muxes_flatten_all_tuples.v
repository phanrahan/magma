module aggregate_mux_wrapper(
  input  [7:0] a_x,
  input        a_y,
               s,
  output [7:0] y_x,
  output       y_y
);

  wire [1:0][7:0] _GEN = {{~a_x}, {a_x}};
  wire [1:0]      _GEN_0 = {{~a_y}, {a_y}};
  assign y_x = _GEN[s];
  assign y_y = _GEN_0[s];
endmodule

