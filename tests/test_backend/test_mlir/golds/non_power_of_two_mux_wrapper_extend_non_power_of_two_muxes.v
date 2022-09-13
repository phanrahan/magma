module non_power_of_two_mux_wrapper(	// <stdin>:1:1
  input  struct packed {logic [7:0] x; logic y; } a,
  input  [3:0]                                    s,
  output struct packed {logic [7:0] x; logic y; } y);

wire [7:0] _T = a.x;	// <stdin>:2:10
wire _T_0 = a.y;	// <stdin>:5:10
wire struct packed {logic [7:0] x; logic y; } _T_1 = '{x: (~_T), y: (~_T_0)};	// <stdin>:4:10, :7:10, :8:10
wire struct packed {logic [7:0] x; logic y; } _T_2 = '{x: (~_T), y: (~_T_0)};	// <stdin>:4:10, :7:10, :9:10
wire struct packed {logic [7:0] x; logic y; } _T_3 = '{x: (~_T), y: (~_T_0)};	// <stdin>:4:10, :7:10, :10:10
wire struct packed {logic [7:0] x; logic y; } _T_4 = '{x: (~_T), y: (~_T_0)};	// <stdin>:4:10, :7:10, :11:10
wire struct packed {logic [7:0] x; logic y; } _T_5 = '{x: (~_T), y: (~_T_0)};	// <stdin>:4:10, :7:10, :12:11
wire struct packed {logic [7:0] x; logic y; } _T_6 = '{x: (~_T), y: (~_T_0)};	// <stdin>:4:10, :7:10, :13:11
wire struct packed {logic [7:0] x; logic y; } _T_7 = '{x: (~_T), y: (~_T_0)};	// <stdin>:4:10, :7:10, :14:11
wire struct packed {logic [7:0] x; logic y; } _T_8 = '{x: (~_T), y: (~_T_0)};	// <stdin>:4:10, :7:10, :15:11
wire struct packed {logic [7:0] x; logic y; } _T_9 = '{x: (~_T), y: (~_T_0)};	// <stdin>:4:10, :7:10, :16:11
wire struct packed {logic [7:0] x; logic y; } _T_10 = '{x: (~_T), y: (~_T_0)};	// <stdin>:4:10, :7:10, :17:11
wire struct packed {logic [7:0] x; logic y; } _T_11 = '{x: (~_T), y: (~_T_0)};	// <stdin>:4:10, :7:10, :18:11
wire struct packed {logic [7:0] x; logic y; }[15:0] _T_12 = {{_T_11}, {_T_11}, {_T_11}, {_T_11}, {_T_11}, {_T_10}, {_T_9}, {_T_8}, {_T_7}, {_T_6},
                {_T_5}, {_T_4}, {_T_3}, {_T_2}, {_T_1}, {a}};	// <stdin>:19:11
  assign y = _T_12[s];	// <stdin>:20:11, :21:5
endmodule

