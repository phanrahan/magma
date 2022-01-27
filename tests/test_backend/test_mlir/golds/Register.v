module Register(
  input  struct packed {logic [7:0] x; logic y; } I,
  input                                           CLK,
  output struct packed {logic [7:0] x; logic y; } O);

  reg [8:0] reg_P9_inst0;	// <stdin>:21:21

  wire [7:0] _T = I.x;	// <stdin>:3:10
  wire [7:0] _T_0 = I.x;	// <stdin>:5:10
  wire [7:0] _T_1 = I.x;	// <stdin>:7:10
  wire [7:0] _T_2 = I.x;	// <stdin>:9:10
  wire [7:0] _T_3 = I.x;	// <stdin>:11:10
  wire [7:0] _T_4 = I.x;	// <stdin>:13:11
  wire [7:0] _T_5 = I.x;	// <stdin>:15:11
  wire [7:0] _T_6 = I.x;	// <stdin>:17:11
  wire [8:0] _T_7 = {I.y, _T_6[7], _T_5[6], _T_4[5], _T_3[4], _T_2[3], _T_1[2], _T_0[1], _T[0]};	// <stdin>:4:10, :6:10, :8:10, :10:10, :12:10, :14:11, :16:11, :18:11, :19:11, :20:11
  always @(posedge CLK)	// <stdin>:22:5
    reg_P9_inst0 <= _T_7;	// <stdin>:23:7
  initial	// <stdin>:25:5
    reg_P9_inst0 = 9'h106;	// <stdin>:26:19, :27:7
  wire [8:0] _T_8 = reg_P9_inst0;	// <stdin>:29:11
  wire struct packed {logic [7:0] x; logic y; } _T_9 = '{x: (_T_8[7:0]), y: (_T_8[8])};	// <stdin>:30:11, :31:11, :32:11
  assign O = _T_9;	// <stdin>:33:5
endmodule

