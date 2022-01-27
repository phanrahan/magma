module ByteSelector(	// <stdin>:1:1
  input  [31:0] I,
  input  [1:0]  offset,
  output [7:0]  O);

wire [1:0][7:0] _T = {{I[31:24]}, {I[23:16]}};	// <stdin>:10:10, :19:11, :22:11
wire [1:0][7:0] _T_0 = {{_T[offset == 2'h2]}, {I[15:8]}};	// <stdin>:20:11, :21:11, :23:11, :32:11, :35:11
wire [1:0][7:0] _T_1 = {{_T_0[offset == 2'h1]}, {I[7:0]}};	// <stdin>:33:11, :34:11, :36:11, :45:11, :48:11
  assign O = _T_1[offset == 2'h0];	// <stdin>:46:11, :47:11, :49:11, :50:5
endmodule

