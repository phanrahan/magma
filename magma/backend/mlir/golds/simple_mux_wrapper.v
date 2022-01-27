module simple_mux_wrapper(	// <stdin>:1:1
  input  [7:0] a,
  input        s,
  output [7:0] y);

wire [1:0][7:0] _T = {{a}, {~a}};	// <stdin>:3:10, :4:10
  assign y = _T[s];	// <stdin>:5:10, :6:5
endmodule

