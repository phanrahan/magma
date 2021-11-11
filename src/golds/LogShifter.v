module LogShifter(
  input  [15:0] I,
  input  [3:0]  shift_amount,
  input         CLK,
  output [15:0] O);

  reg [15:0] Register_inst0;	// <stdin>:11:23
  reg [15:0] Register_inst1;	// <stdin>:17:23
  reg [15:0] Register_inst2;	// <stdin>:23:23

  wire [15:0] _T = ({{I}, {I << 16'h8}})[shift_amount[3]];	// <stdin>:6:15, :7:10, :8:10, :9:10, :10:10
  wire [15:0] _T_0 = Register_inst0;	// <stdin>:12:10
  wire [15:0] _T_1 = ({{_T_0}, {_T_0 << 16'h4}})[shift_amount[2]];	// <stdin>:5:15, :13:10, :14:10, :15:10, :16:10
  wire [15:0] _T_2 = Register_inst1;	// <stdin>:18:10
  wire [15:0] _T_3 = ({{_T_2}, {_T_2 << 16'h2}})[shift_amount[1]];	// <stdin>:4:15, :19:11, :20:11, :21:11, :22:11
  always @(posedge CLK) begin	// <stdin>:24:5
    Register_inst0 <= _T;	// <stdin>:25:7
    Register_inst1 <= _T_1;	// <stdin>:26:7
    Register_inst2 <= _T_3;	// <stdin>:27:7
  end // always @(posedge)
  initial begin	// <stdin>:29:5
    Register_inst0 = 16'h0;	// <stdin>:30:17, :31:7
    Register_inst1 = 16'h0;	// <stdin>:30:17, :32:7
    Register_inst2 = 16'h0;	// <stdin>:30:17, :33:7
  end // initial
  wire [15:0] _T_4 = Register_inst2;	// <stdin>:35:11
  assign O = ({{_T_4}, {_T_4 << 16'h1}})[shift_amount[0]];	// <stdin>:3:15, :36:11, :37:11, :38:11, :39:11, :40:5
endmodule

