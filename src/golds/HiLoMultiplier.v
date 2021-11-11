module HiLoMultiplier(
  input  [15:0] A, B,
  output [15:0] Hi, Lo);

  wire [31:0] _T = {16'h0, A} * {16'h0, B};	// <stdin>:3:15, :4:10, :5:10, :6:10
  assign Hi = _T[31:16];	// <stdin>:7:10, :9:5
  assign Lo = _T[15:0];	// <stdin>:8:10, :9:5
endmodule

