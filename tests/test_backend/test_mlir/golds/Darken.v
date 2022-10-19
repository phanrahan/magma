module Darken(
  input  [7:0] I,
  output [7:0] O);

  assign O = {I[6:0], 1'h0};
endmodule

