module aggregate_mux_wrapper(	// <stdin>:1:1
  input  struct packed {logic [7:0] x; logic y; } a,
  input                                           s,
  output struct packed {logic [7:0] x; logic y; } y);

wire struct packed {logic [7:0] x; logic y; } _T = '{x: (~a.x), y: (~a.y)};	// <stdin>:2:10, :4:10, :5:10, :7:10, :8:10
wire struct packed {logic [7:0] x; logic y; }[1:0] _T_0 = {{a}, {_T}};	// <stdin>:9:10
  assign y = _T_0[s];	// <stdin>:10:10, :11:5
endmodule

