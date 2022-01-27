module simple_aggregates_bits(	// <stdin>:1:1
  input  [15:0] a,
  output [15:0] y);

  assign y = {a[7:0], a[15:8]};	// <stdin>:18:11, :19:5
endmodule

