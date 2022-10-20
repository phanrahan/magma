module ByteSelector(
  input  [31:0] I,
  input  [1:0]  offset,
  output [7:0]  O);

wire [1:0][7:0] _T = {{I[31:24]}, {I[23:16]}};
wire [1:0][7:0] _T_0 = {{_T[offset == 2'h2]}, {I[15:8]}};
wire [1:0][7:0] _T_1 = {{_T_0[offset == 2'h1]}, {I[7:0]}};
  assign O = _T_1[offset == 2'h0];
endmodule

