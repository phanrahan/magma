module SimpleALU(
  input  [3:0] a, b,
  input  [1:0] opcode,
  output [3:0] out);

wire [1:0][3:0] _T = {{b}, {a}};
wire [1:0][3:0] _T_0 = {{_T[opcode == 2'h2]}, {a - b}};
wire [1:0][3:0] _T_1 = {{_T_0[opcode == 2'h1]}, {a + b}};
  assign out = _T_1[opcode == 2'h0];
endmodule

