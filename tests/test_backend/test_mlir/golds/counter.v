module counter(	// <stdin>:1:1
  input         CLK,
  output [15:0] y);

  reg [15:0] Register_inst0;	// <stdin>:4:10

  always_ff @(posedge CLK)	// <stdin>:5:5
    Register_inst0 <= Register_inst0 + 16'h1;	// <stdin>:2:10, :3:10, :6:9, :12:10
  initial	// <stdin>:9:5
    Register_inst0 = 16'h0;	// <stdin>:8:10, :10:9
  assign y = Register_inst0;	// <stdin>:12:10, :13:5
endmodule

