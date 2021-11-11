module simple_array_of_bit(
  input  [7:0] I,
  output [7:0] O);

  assign O = {I[0], I[1], I[2], I[3], I[4], I[5], I[6], I[7]};	// <stdin>:3:10, :4:10, :5:10, :6:10, :7:10, :8:10, :9:10, :10:10, :11:10, :12:5
endmodule

