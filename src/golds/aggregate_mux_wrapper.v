module aggregate_mux_wrapper(
  input  struct packed {logic [7:0] x; logic y; } a,
  input                                           s,
  output struct packed {logic [7:0] x; logic y; } y);

  wire struct packed {logic [7:0] x; logic y; } _T = '{x: (~a.x), y: (~a.y)};	// <stdin>:5:10, :6:10, :7:10, :8:10, :9:10
  assign y = ({{a}, {_T}})[s];	// <stdin>:10:10, :11:10, :12:5
endmodule

