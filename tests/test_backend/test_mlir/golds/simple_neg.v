module simple_neg(
  input  [7:0] a,
  output [7:0] y
);

  assign y = 8'h0 - a;
endmodule

