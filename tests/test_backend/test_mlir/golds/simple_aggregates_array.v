module simple_aggregates_array(	// <stdin>:1:1
  input  [7:0][15:0] a,
  output [7:0][15:0] y,
  output [3:0][15:0] z);

wire [15:0] _T = a[3'h4];	// <stdin>:2:10, :3:10
wire [15:0] _T_0 = a[3'h5];	// <stdin>:4:10, :5:10
wire [15:0] _T_1 = a[3'h6];	// <stdin>:6:10, :7:10
wire [15:0] _T_2 = a[3'h7];	// <stdin>:8:10, :9:10
wire [15:0] _T_3 = a[3'h0];	// <stdin>:10:10, :11:10
wire [15:0] _T_4 = a[3'h1];	// <stdin>:12:11, :13:11
wire [15:0] _T_5 = a[3'h2];	// <stdin>:14:11, :15:11
wire [15:0] _T_6 = a[3'h3];	// <stdin>:16:11, :17:11
wire [7:0][15:0] _T_7 = {{_T_6}, {_T_5}, {_T_4}, {_T_3}, {_T_2}, {_T_1}, {_T_0}, {_T}};	// <stdin>:19:11
  assign y = {{_T_6}, {_T_5}, {_T_4}, {_T_3}, {_T_2}, {_T_1}, {_T_0}, {_T}};	// <stdin>:18:11, :22:5
  assign z = {{_T_6}, {_T_5}, {_T_4}, {_T_7[3'h4]}};	// <stdin>:2:10, :20:11, :21:11, :22:5
endmodule

