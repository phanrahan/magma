module Mux2xBits8(
  input  [7:0] I0, I1,
  input        S,
  output [7:0] O);

  wire struct packed {logic [1:0][7:0] data; logic sel; } _T = '{data: ({{I1}, {I0}}), sel: S};	// <stdin>:3:10, :4:10
  assign O = _T.data[_T.sel];	// <stdin>:5:10, :6:10, :7:10, :8:5
endmodule

