module complex_wire(
  input  [7:0]      I0,
  input             I1,
  input  [3:0][7:0] I2,
  output [7:0]      O0,
  output            O1,
  output [3:0][7:0] O2);

  wire [7:0]  tmp0;	// <stdin>:7:13
  wire        tmp1;	// <stdin>:10:13
  wire [31:0] tmp2;	// <stdin>:18:13

  assign tmp0 = I0;	// <stdin>:8:5
  assign tmp1 = I1;	// <stdin>:11:5
  assign tmp2 = {I2[2'h3], I2[2'h2], I2[2'h1], I2[2'h0]};	// <stdin>:3:15, :4:15, :5:14, :6:14, :13:10, :14:10, :15:10, :16:10, :17:10, :19:5
  wire [31:0] _T = tmp2;	// <stdin>:20:10
  assign O0 = tmp0;	// <stdin>:9:10, :26:5
  assign O1 = tmp1;	// <stdin>:12:10, :26:5
  assign O2 = {{_T[31:24]}, {_T[23:16]}, {_T[15:8]}, {_T[7:0]}};	// <stdin>:21:10, :22:10, :23:11, :24:11, :25:11, :26:5
endmodule

