module Darken(
  input  [7:0] I,
  output [7:0] O);

  assign O = I << 8'h1;	// <stdin>:3:14, :4:10, :5:5
endmodule

