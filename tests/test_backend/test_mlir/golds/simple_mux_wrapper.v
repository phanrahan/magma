module simple_mux_wrapper(
  input  [7:0] a,
  input        s,
  output [7:0] y
);

  wire [1:0][7:0] _GEN = {{~a}, {a}};
  assign y = _GEN[s];
endmodule

