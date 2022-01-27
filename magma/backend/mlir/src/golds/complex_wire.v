module complex_wire(	// <stdin>:1:1
  input  [7:0]      I0,
  input             I1,
  input  [3:0][7:0] I2,
  output [7:0]      O0,
  output            O1,
  output [3:0][7:0] O2);

  wire [7:0]  tmp0;	// <stdin>:2:10
  wire        tmp1;	// <stdin>:5:10
  wire [31:0] tmp2;	// <stdin>:49:11

  assign tmp0 = I0;	// <stdin>:3:5
  assign tmp1 = I1;	// <stdin>:6:5
  assign tmp2 = {I2[2'h3], I2[2'h2], I2[2'h1], I2[2'h0]};	// <stdin>:8:10, :9:10, :18:11, :19:11, :28:11, :29:11, :38:11, :39:11, :48:11, :50:5
  assign O0 = tmp0;	// <stdin>:4:10, :89:5
  assign O1 = tmp1;	// <stdin>:7:10, :89:5
  assign O2 = {{tmp2[31:24]}, {tmp2[23:16]}, {tmp2[15:8]}, {tmp2[7:0]}};	// <stdin>:51:11, :60:11, :69:11, :78:11, :87:11, :88:11, :89:5
endmodule

