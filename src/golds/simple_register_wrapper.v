module simple_register_wrapper(
  input  [7:0] a,
  input        CLK,
  output [7:0] y);

  reg [7:0] reg0;	// <stdin>:3:13

  always @(posedge CLK)	// <stdin>:4:5
    reg0 <= a;	// <stdin>:5:7
  initial	// <stdin>:7:5
    reg0 = 8'h3;	// <stdin>:8:16, :9:7
  assign y = reg0;	// <stdin>:11:10, :12:5
endmodule

