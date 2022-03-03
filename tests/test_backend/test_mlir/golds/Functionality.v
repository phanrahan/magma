module clb(	// <stdin>:1:1
  input  [15:0] a, b, c, d,
  output [15:0] O);

  assign O = a & b | ~c & d;	// <stdin>:2:10, :4:10, :5:10, :6:10, :7:5
endmodule

module Functionality(	// <stdin>:9:1
  input  [15:0] x, y,
  output [15:0] z);

  clb clb_inst0 (	// <stdin>:10:10
    .a (x),
    .b (y),
    .c (x),
    .d (y),
    .O (z)
  );
endmodule

