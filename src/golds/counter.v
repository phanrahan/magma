module counter(
  input         CLK,
  output [15:0] y);

  wire [15:0] _T;	// <stdin>:13:10
  reg  [15:0] Register_inst0;	// <stdin>:5:23

  wire [15:0] _T_0 = _T + 16'h1;	// <stdin>:3:15, :4:10, :13:10
  always @(posedge CLK)	// <stdin>:6:5
    Register_inst0 <= _T_0;	// <stdin>:7:7
  initial	// <stdin>:9:5
    Register_inst0 = 16'h0;	// <stdin>:10:17, :11:7
  assign _T = Register_inst0;	// <stdin>:13:10
  assign y = _T;	// <stdin>:13:10, :14:5
endmodule

