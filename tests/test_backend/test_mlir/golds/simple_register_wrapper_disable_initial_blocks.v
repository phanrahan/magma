module simple_register_wrapper(	// <stdin>:1:1
  input  [7:0] a,
  input        CLK,
  output [7:0] y);

  reg [7:0] reg0;	// <stdin>:2:10

  always_ff @(posedge CLK)	// <stdin>:3:5
    reg0 <= a;	// <stdin>:4:9
  assign y = reg0;	// <stdin>:7:10, :8:5
endmodule

