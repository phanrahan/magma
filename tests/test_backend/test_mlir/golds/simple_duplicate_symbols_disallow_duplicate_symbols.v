module simple_duplicate_symbols(
  input        I,
  output [1:0] O
);

  wire x = I;
  wire x_0 = I;
  assign O = {x_0, x};
endmodule

