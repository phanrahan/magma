module Register(
  input  struct packed {logic [7:0] x; logic y; } I,
  input                                           CLK,
  output struct packed {logic [7:0] x; logic y; } O);

  reg [8:0] reg_P9_inst0;

  wire [7:0] _T = I.x;
  wire [7:0] _T_0 = I.x;
  wire [7:0] _T_1 = I.x;
  wire [7:0] _T_2 = I.x;
  wire [7:0] _T_3 = I.x;
  wire [7:0] _T_4 = I.x;
  wire [7:0] _T_5 = I.x;
  wire [7:0] _T_6 = I.x;
  wire [8:0] _T_7 = {I.y, _T_6[7], _T_5[6], _T_4[5], _T_3[4], _T_2[3], _T_1[2], _T_0[1], _T[0]};
  always @(posedge CLK)
    reg_P9_inst0 <= _T_7;
  initial
    reg_P9_inst0 = 9'h106;
  wire [8:0] _T_8 = reg_P9_inst0;
  wire struct packed {logic [7:0] x; logic y; } _T_9 = '{x: (_T_8[7:0]), y: (_T_8[8])};
  assign O = _T_9;
endmodule

