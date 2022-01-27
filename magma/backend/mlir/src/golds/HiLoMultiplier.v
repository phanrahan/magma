module HiLoMultiplier(	// <stdin>:1:1
  input  [15:0] A, B,
  output [15:0] Hi, Lo);

wire [31:0] _T = {16'h0, A} * {16'h0, B};	// <stdin>:34:11, :67:11, :68:11
  assign Hi = _T[31:16];	// <stdin>:85:11, :103:5
  assign Lo = _T[15:0];	// <stdin>:102:12, :103:5
endmodule

