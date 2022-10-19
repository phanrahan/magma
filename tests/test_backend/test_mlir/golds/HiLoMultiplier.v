module HiLoMultiplier(
  input  [15:0] A, B,
  output [15:0] Hi, Lo);

wire [31:0] _T = {16'h0, A} * {16'h0, B};
  assign Hi = _T[31:16];
  assign Lo = _T[15:0];
endmodule

