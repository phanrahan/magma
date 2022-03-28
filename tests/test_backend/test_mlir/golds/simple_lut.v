module LUT(	// <stdin>:1:1
  input  [1:0] I,
  output [7:0] O);

wire [3:0] _T = {{1'h1}, {1'h0}, {1'h1}, {1'h0}};	// <stdin>:2:10, :3:10, :4:10
wire [3:0] _T_0 = {{1'h1}, {1'h1}, {1'h0}, {1'h1}};	// <stdin>:2:10, :3:10, :6:10
wire [3:0] _T_1 = {{1'h1}, {1'h1}, {1'h1}, {1'h1}};	// <stdin>:2:10, :8:10
wire [3:0] _T_2 = {{1'h1}, {1'h1}, {1'h1}, {1'h1}};	// <stdin>:2:10, :10:10
wire [3:0] _T_3 = {{1'h0}, {1'h1}, {1'h0}, {1'h1}};	// <stdin>:2:10, :3:10, :12:11
wire [3:0] _T_4 = {{1'h1}, {1'h1}, {1'h1}, {1'h0}};	// <stdin>:2:10, :3:10, :14:11
wire [3:0] _T_5 = {{1'h1}, {1'h0}, {1'h0}, {1'h1}};	// <stdin>:2:10, :3:10, :16:11
wire [3:0] _T_6 = {{1'h1}, {1'h1}, {1'h1}, {1'h1}};	// <stdin>:2:10, :18:11
  assign O = {_T_6[I], _T_5[I], _T_4[I], _T_3[I], _T_2[I], _T_1[I], _T_0[I], _T[I]};	// <stdin>:5:10, :7:10, :9:10, :11:10, :13:11, :15:11, :17:11, :19:11, :20:11, :21:5
endmodule

module simple_lut(	// <stdin>:23:1
  input  [1:0] a,
  output [7:0] y);

  LUT LUT_inst0 (	// <stdin>:24:10
    .I (a),
    .O (y)
  );
endmodule
