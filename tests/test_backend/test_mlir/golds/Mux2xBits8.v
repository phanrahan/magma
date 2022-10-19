module Mux2xBits8(
  input  [7:0] I0, I1,
  input        S,
  output [7:0] O);

  wire struct packed {logic [1:0][7:0] data; logic sel; } _T = '{data: ({{I1}, {I0}}), sel: S};
  assign O = _T.data[_T.sel];
endmodule

