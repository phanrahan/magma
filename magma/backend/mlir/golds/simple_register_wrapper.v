module simple_register_wrapper(	// <stdin>:1:1
  input  [7:0] a,
  input        CLK,
  output [7:0] y);

  reg [7:0] reg0;	// <stdin>:2:10

  always_ff @(posedge CLK)	// <stdin>:3:5
    reg0 <= a;	// <stdin>:4:9
  initial	// <stdin>:7:5
    reg0 = 8'h3;	// <stdin>:6:10, :8:9
  assign y = reg0;	// <stdin>:10:10, :11:5
endmodule

