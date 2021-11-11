module VecSearch(
  input        CLK,
  output [3:0] out);

  wire [2:0] _T;	// <stdin>:20:10
  reg  [2:0] Register_inst0;	// <stdin>:12:23

  wire [2:0] _T_0 = _T + 3'h1;	// <stdin>:3:14, :11:10, :20:10
  always @(posedge CLK)	// <stdin>:13:5
    Register_inst0 <= _T_0;	// <stdin>:14:7
  initial	// <stdin>:16:5
    Register_inst0 = 3'h0;	// <stdin>:17:16, :18:7
  assign _T = Register_inst0;	// <stdin>:20:10
  assign out = ({{4'h0}, {4'h4}, {4'hF}, {4'hE}, {4'h2}, {4'h5}, {4'hD}})[_T];	// <stdin>:4:15, :5:14, :6:14, :7:15, :8:15, :9:14, :10:14, :20:10, :21:10, :22:10, :23:5
endmodule

