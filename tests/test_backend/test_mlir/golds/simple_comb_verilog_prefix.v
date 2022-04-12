module proj_simple_comb(	// <stdin>:1:1
  input  [15:0] a, b, c,
  output [15:0] y, z);

  assign y = 16'hFFFF;	// <stdin>:2:10, :6:5
  assign z = 16'hFFFF;	// <stdin>:2:10, :6:5
endmodule

