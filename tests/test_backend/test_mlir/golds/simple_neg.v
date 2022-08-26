module simple_neg(	// <stdin>:1:1
  input  [7:0] a,
  output [7:0] y);

  assign y = 8'h0 - a;	// <stdin>:2:10, :3:10, :4:5
endmodule

