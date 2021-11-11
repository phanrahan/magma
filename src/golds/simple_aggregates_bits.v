module simple_aggregates_bits(
  input  [15:0] a,
  output [15:0] y);

  assign y = {a[7:0], a[15:8]};	// <stdin>:3:10, :4:10, :5:10, :6:5
endmodule

