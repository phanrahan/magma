module GCD(
  input  [15:0] a, b,
  input         load, CLK,
  output [15:0] O0,
  output        O1);

  wire [15:0] _T;	// <stdin>:35:11
  wire [15:0] _T_0;	// <stdin>:16:11
  reg  [15:0] Register_inst1;	// <stdin>:15:23
  reg  [15:0] Register_inst0;	// <stdin>:25:23

  wire _T_1 = _T_0 < _T;	// <stdin>:6:10, :16:11, :35:11
  wire _T_2 = _T_0 == 16'h0;	// <stdin>:4:15, :9:10, :16:11
  wire [15:0] _tmp = ({{_T_0}, {({{_T_0 - _T}, {_T_0}})[_T_1]}})[~_T_2];	// <stdin>:5:10, :7:10, :8:10, :10:10, :11:10, :12:10, :16:11, :35:11
  wire [15:0] _T_3 = ({{_tmp}, {b}})[load];	// <stdin>:5:10, :7:10, :8:10, :10:10, :11:10, :13:10, :14:10, :16:11, :35:11
  assign _T_0 = Register_inst1;	// <stdin>:16:11
  wire [15:0] _tmp_5 = ({{_T}, {({{_T}, {_T - _T_0}})[_T_1]}})[~_T_2];	// <stdin>:16:11, :17:11, :18:11, :19:11, :20:11, :21:11, :22:11, :35:11
  wire [15:0] _T_4 = ({{_tmp_5}, {a}})[load];	// <stdin>:16:11, :17:11, :18:11, :19:11, :20:11, :21:11, :23:11, :24:11, :35:11
  always @(posedge CLK) begin	// <stdin>:26:5
    Register_inst1 <= _T_3;	// <stdin>:27:7
    Register_inst0 <= _T_4;	// <stdin>:28:7
  end // always @(posedge)
  initial begin	// <stdin>:30:5
    Register_inst1 = 16'h0;	// <stdin>:31:19, :32:7
    Register_inst0 = 16'h0;	// <stdin>:31:19, :33:7
  end // initial
  assign _T = Register_inst0;	// <stdin>:35:11
  assign O0 = _T;	// <stdin>:35:11, :37:5
  assign O1 = _T_0 == 16'h0;	// <stdin>:4:15, :16:11, :36:11, :37:5
endmodule

