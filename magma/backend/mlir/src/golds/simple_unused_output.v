module simple_comb(	// <stdin>:1:1
  input  [15:0] a, b, c,
  output [15:0] y, z);

  assign y = 16'hFFFF;	// <stdin>:2:10, :6:5
  assign z = 16'hFFFF;	// <stdin>:2:10, :6:5
endmodule

module simple_unused_output(	// <stdin>:8:1
  input  [15:0] a, b, c,
  output [15:0] y);

  wire [15:0] simple_comb_inst0_y;	// <stdin>:9:14

  simple_comb simple_comb_inst0 (	// <stdin>:9:14
    .a (a),
    .b (b),
    .c (c),
    .y (simple_comb_inst0_y),
    .z (y)
  );
endmodule

