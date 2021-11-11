module Cell(
  input  [7:0] neighbors,
  input        running, write_enable, write_value, CLK,
  output       out);

  wire _T;	// <stdin>:52:11
  reg  Register_inst0;	// <stdin>:44:23

  wire [2:0] _tmp = {2'h0, neighbors[0]} + {2'h0, neighbors[1]} + {2'h0, neighbors[2]} + {2'h0, neighbors[3]};	// <stdin>:6:14, :10:10, :11:10, :12:10, :13:10, :14:10, :15:10, :16:10, :17:10, :26:11
  wire [2:0] _tmp_2 = {2'h0, neighbors[4]} + {2'h0, neighbors[5]} + {2'h0, neighbors[6]} + {2'h0, neighbors[7]};	// <stdin>:6:14, :18:10, :19:11, :20:11, :21:11, :22:11, :23:11, :24:11, :25:11, :26:11
  wire [2:0] _T_0 = _tmp + _tmp_2;	// <stdin>:6:14, :10:10, :11:10, :12:10, :13:10, :14:10, :15:10, :16:10, :17:10, :18:10, :19:11, :20:11, :21:11, :22:11, :23:11, :24:11, :25:11, :26:11
  wire _tmp_3 = ({{({{1'h0}, {1'h1}})[_T_0 < 3'h4]}, {1'h0}})[_T_0 < 3'h2];	// <stdin>:3:14, :4:15, :7:13, :8:14, :31:11, :32:11, :33:11, :34:11, :35:11, :36:11
  wire _tmp_4 = ({{({{1'h0}, {1'h1}})[~_T & _T_0 == 3'h3]}, {_tmp_3}})[_T];	// <stdin>:5:14, :7:13, :8:14, :9:10, :27:11, :28:11, :29:11, :30:11, :37:11, :38:11, :52:11
  wire _T_1 = ({{_tmp_4}, {({{_T}, {write_value}})[write_enable]}})[~running];	// <stdin>:3:14, :4:15, :5:14, :7:13, :8:14, :9:10, :27:11, :28:11, :29:11, :30:11, :31:11, :32:11, :33:11, :34:11, :35:11, :37:11, :39:11, :40:11, :41:11, :42:11, :43:11, :52:11
  always @(posedge CLK)	// <stdin>:45:5
    Register_inst0 <= _T_1;	// <stdin>:46:7
  initial	// <stdin>:48:5
    Register_inst0 = 1'h0;	// <stdin>:49:18, :50:7
  assign _T = Register_inst0;	// <stdin>:52:11
  assign out = _T;	// <stdin>:52:11, :53:5
endmodule

