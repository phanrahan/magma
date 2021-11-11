module clb(
  input  [15:0] a, b, c, d,
  output [15:0] O);

  assign O = a & b | ~c & d;	// <stdin>:4:10, :5:10, :6:10, :7:10, :8:5
endmodule

module Functionality(
  input  [15:0] x, y,
  output [15:0] z);

  clb clb_inst0 (	// <stdin>:11:20
    .a (x),
    .b (y),
    .c (x),
    .d (y),
    .O (z)
  );
endmodule

