module SimpleALU(
  input  [3:0] a, b,
  input  [1:0] opcode,
  output [3:0] out);

  wire [3:0] _tmp = ({{({{b}, {a}})[opcode == 2'h2]}, {a - b}})[opcode == 2'h1];	// <stdin>:4:14, :5:15, :6:10, :7:10, :8:10, :9:10, :10:10, :11:10, :12:10
  assign out = ({{_tmp}, {a + b}})[opcode == 2'h0];	// <stdin>:3:14, :4:14, :5:15, :6:10, :7:10, :8:10, :9:10, :10:10, :11:10, :13:10, :14:10, :15:10, :16:11, :17:5
endmodule

