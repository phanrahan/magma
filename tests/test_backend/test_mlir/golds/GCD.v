module GCD(	// <stdin>:1:1
  input  [15:0] a, b,
  input         load, CLK,
  output [15:0] O0,
  output        O1);

  reg [15:0] Register_inst1;	// <stdin>:14:11
  reg [15:0] Register_inst0;	// <stdin>:30:11

  always_ff @(posedge CLK) begin	// <stdin>:31:5
    automatic logic             _T = Register_inst1 < Register_inst0;	// <stdin>:3:10, :22:10, :37:10
    automatic logic [1:0][15:0] _T_0 = {{Register_inst1 - Register_inst0}, {Register_inst1}};	// <stdin>:2:10, :4:10, :22:10, :37:10
    automatic logic [1:0][15:0] _T_1 = {{Register_inst1}, {_T_0[_T]}};	// <stdin>:5:10, :10:11, :22:10
    automatic logic [1:0][15:0] _T_2 = {{_T_1[|Register_inst1]}, {b}};	// <stdin>:7:10, :11:11, :12:11, :22:10
    automatic logic [1:0][15:0] _T_3 = {{Register_inst0}, {Register_inst0 - Register_inst1}};	// <stdin>:22:10, :23:11, :24:11, :37:10
    automatic logic [1:0][15:0] _T_4 = {{Register_inst0}, {_T_3[_T]}};	// <stdin>:25:11, :26:11, :37:10
    automatic logic [1:0][15:0] _T_5 = {{_T_4[|Register_inst1]}, {a}};	// <stdin>:7:10, :22:10, :27:11, :28:11

    Register_inst1 <= _T_2[load];	// <stdin>:13:11, :16:9
    Register_inst0 <= _T_5[load];	// <stdin>:29:11, :32:9
  end // always_ff @(posedge)
  initial begin	// <stdin>:34:5
    Register_inst1 = 16'h0;	// <stdin>:6:10, :20:9
    Register_inst0 = 16'h0;	// <stdin>:6:10, :35:9
  end // initial
  assign O0 = Register_inst0;	// <stdin>:37:10, :40:5
  assign O1 = Register_inst1 == 16'h0;	// <stdin>:6:10, :22:10, :39:11, :40:5
endmodule

