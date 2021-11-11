module simple_comb(
  input  [15:0] a, b, c,
  output [15:0] y, z);

  wire [15:0] _T = a | ~a | b;	// <stdin>:4:10, :5:10
  assign y = _T;	// <stdin>:6:5
  assign z = _T;	// <stdin>:6:5
endmodule

module simple_unused_output(
  input  [15:0] a, b, c,
  output [15:0] y);

  wire [15:0] simple_comb_inst0_y;	// <stdin>:9:50

  simple_comb simple_comb_inst0 (	// <stdin>:9:50
    .a (a),
    .b (b),
    .c (c),
    .y (simple_comb_inst0_y),
    .z (y)
  );
endmodule

