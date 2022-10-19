module clb(
  input  [15:0] a, b, c, d,
  output [15:0] O);

  assign O = a & b | ~c & d;
endmodule

module Functionality(
  input  [15:0] x, y,
  output [15:0] z);

  clb clb_inst0 (
    .a (x),
    .b (y),
    .c (x),
    .d (y),
    .O (z)
  );
endmodule

