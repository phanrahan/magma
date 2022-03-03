module LogShifter(	// <stdin>:1:1
  input  [15:0] I,
  input  [3:0]  shift_amount,
  input         CLK,
  output [15:0] O);

  reg [15:0] Register_inst0;	// <stdin>:11:11
  reg [15:0] Register_inst1;	// <stdin>:28:11
  reg [15:0] Register_inst2;	// <stdin>:44:11

  always_ff @(posedge CLK) begin	// <stdin>:45:5
    automatic logic [1:0][15:0] _T_0 = {{I}, {{I[7:0], 8'h0}}};	// <stdin>:3:10, :9:10
    automatic logic [1:0][15:0] _T_1 = {{Register_inst0}, {{Register_inst0[11:0], 4'h0}}};	// <stdin>:19:10, :21:11, :26:11
    automatic logic [1:0][15:0] _T_2 = {{Register_inst1}, {{Register_inst1[13:0], 2'h0}}};	// <stdin>:35:11, :37:11, :42:11

    Register_inst0 <= _T_0[shift_amount[3]];	// <stdin>:4:10, :10:10, :13:9
    Register_inst1 <= _T_1[shift_amount[2]];	// <stdin>:22:11, :27:11, :30:9
    Register_inst2 <= _T_2[shift_amount[1]];	// <stdin>:38:11, :43:11, :46:9
  end // always_ff @(posedge)
  initial begin	// <stdin>:48:5
    Register_inst0 = 16'h0;	// <stdin>:15:11, :17:9
    Register_inst1 = 16'h0;	// <stdin>:15:11, :33:9
    Register_inst2 = 16'h0;	// <stdin>:15:11, :49:9
  end // initial
  wire [1:0][15:0] _T = {{Register_inst2}, {{Register_inst2[14:0], 1'h0}}};	// <stdin>:51:11, :53:11, :58:11
  assign O = _T[shift_amount[0]];	// <stdin>:54:11, :59:11, :60:5
endmodule

