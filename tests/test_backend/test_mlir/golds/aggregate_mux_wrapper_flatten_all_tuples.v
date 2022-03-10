module aggregate_mux_wrapper(	// <stdin>:1:1
  input  [7:0] a_x,
  input        a_y, s,
  output [7:0] y_x,
  output       y_y);

wire [1:0][7:0] _T = {{a_x}, {~a_x}};	// <stdin>:3:10, :6:10
wire [1:0] _T_0 = {{a_y}, {~a_y}};	// <stdin>:5:10, :8:10
  assign y_x = _T[s];	// <stdin>:7:10, :10:5
  assign y_y = _T_0[s];	// <stdin>:9:10, :10:5
endmodule

