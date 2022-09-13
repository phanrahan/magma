module simple_aggregates_product(	// <stdin>:1:1
  input  [7:0] a_x, a_y,
  output [7:0] y_x, y_y);

  assign y_x = ~a_x;	// <stdin>:3:10, :5:5
  assign y_y = ~a_y;	// <stdin>:4:10, :5:5
endmodule

