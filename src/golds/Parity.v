module Parity(
  input  I, CLK,
  output O);

  wire _T;	// <stdin>:18:10
  reg  Register_inst0;	// <stdin>:10:23

  wire _T_0 = ({{_T}, {({{1'h0}, {1'h1}})[~_T]}})[I];	// <stdin>:3:13, :4:14, :5:10, :6:10, :7:10, :8:10, :9:10, :18:10
  always @(posedge CLK)	// <stdin>:11:5
    Register_inst0 <= _T_0;	// <stdin>:12:7
  initial	// <stdin>:14:5
    Register_inst0 = 1'h0;	// <stdin>:15:18, :16:7
  assign _T = Register_inst0;	// <stdin>:18:10
  assign O = _T;	// <stdin>:18:10, :19:5
endmodule

