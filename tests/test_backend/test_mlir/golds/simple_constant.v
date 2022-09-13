module simple_constant(	// <stdin>:1:1
  input  [7:0] I,
  output [7:0] O);

  assign O = {I[6:0], 1'h0};	// <stdin>:3:10, :4:5
endmodule

