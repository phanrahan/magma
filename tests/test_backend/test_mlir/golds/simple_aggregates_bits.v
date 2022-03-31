module simple_aggregates_bits(	// <stdin>:1:1
  input  [15:0] a,
  output [15:0] y,
  output [7:0]  z);

  assign y = {a[7:0], a[15:8]};	// <stdin>:18:11, :22:5
  assign z = a[7:0];	// <stdin>:21:11, :22:5
endmodule

