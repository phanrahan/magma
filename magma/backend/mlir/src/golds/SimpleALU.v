module SimpleALU(	// <stdin>:1:1
  input  [3:0] a, b,
  input  [1:0] opcode,
  output [3:0] out);

wire [1:0][3:0] _T = {{b}, {a}};	// <stdin>:4:10
wire [1:0][3:0] _T_0 = {{_T[opcode == 2'h2]}, {a - b}};	// <stdin>:2:10, :3:10, :5:10, :6:10, :9:10
wire [1:0][3:0] _T_1 = {{_T_0[opcode == 2'h1]}, {a + b}};	// <stdin>:7:10, :8:10, :10:10, :11:10, :14:11
  assign out = _T_1[opcode == 2'h0];	// <stdin>:12:11, :13:11, :15:11, :16:5
endmodule

