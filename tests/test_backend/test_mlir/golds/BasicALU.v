module BasicALU(
  input  [3:0] a, b, opcode,
  output [3:0] out);

wire [1:0][3:0] _T = {{{3'h0, a == b}}, {{3'h0, a < b}}};
wire [1:0][3:0] _T_0 = {{_T[opcode == 4'h8]}, {a - b}};
wire [1:0][3:0] _T_1 = {{_T_0[opcode == 4'h7]}, {a + b}};
wire [1:0][3:0] _T_2 = {{_T_1[opcode == 4'h6]}, {a - 4'h4}};
wire [1:0][3:0] _T_3 = {{_T_2[opcode == 4'h5]}, {a + 4'h4}};
wire [1:0][3:0] _T_4 = {{_T_3[opcode == 4'h4]}, {a - 4'h1}};
wire [1:0][3:0] _T_5 = {{_T_4[opcode == 4'h3]}, {a + 4'h1}};
wire [1:0][3:0] _T_6 = {{_T_5[opcode == 4'h2]}, {b}};
wire [1:0][3:0] _T_7 = {{_T_6[opcode == 4'h1]}, {a}};
  assign out = _T_7[opcode == 4'h0];
endmodule

