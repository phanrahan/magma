module simple_array_slice(	// <stdin>:1:1
  input  [11:0][7:0] a,
  output [3:0][7:0]  y);

  assign y = a[4'h0 +: 4];	// <stdin>:2:10, :3:10, :4:5
endmodule

