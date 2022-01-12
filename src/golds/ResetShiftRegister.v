module ResetShiftRegister(	// <stdin>:1:1
  input  [3:0] I,
  input        shift, CLK, RESETN,
  output [3:0] O);

  reg [3:0] Register_inst0;	// <stdin>:2:10
  reg [3:0] Register_inst1;	// <stdin>:15:10
  reg [3:0] Register_inst2;	// <stdin>:27:10
  reg [3:0] Register_inst3;	// <stdin>:39:10

  always_ff @(posedge CLK) begin	// <stdin>:40:5
    if (RESETN) begin	// <stdin>:40:5
      Register_inst0 <= 4'h0;	// <stdin>:8:9, :10:10
      Register_inst1 <= 4'h0;	// <stdin>:10:10, :21:9
      Register_inst2 <= 4'h0;	// <stdin>:10:10, :33:9
      Register_inst3 <= 4'h0;	// <stdin>:10:10, :45:9
    end
    else begin	// <stdin>:40:5
      if (shift)	// <stdin>:4:9
        Register_inst0 <= I;	// <stdin>:5:13
      if (shift)	// <stdin>:17:9
        Register_inst1 <= Register_inst0;	// <stdin>:14:10, :18:13
      if (shift)	// <stdin>:29:9
        Register_inst2 <= Register_inst1;	// <stdin>:26:10, :30:13
      if (shift)	// <stdin>:41:9
        Register_inst3 <= Register_inst2;	// <stdin>:38:10, :42:13
    end
  end // always_ff @(posedge)
  initial begin	// <stdin>:47:5
    Register_inst0 = 4'h0;	// <stdin>:10:10, :12:9
    Register_inst1 = 4'h0;	// <stdin>:10:10, :24:9
    Register_inst2 = 4'h0;	// <stdin>:10:10, :36:9
    Register_inst3 = 4'h0;	// <stdin>:10:10, :48:9
  end // initial
  assign O = Register_inst3;	// <stdin>:50:10, :51:5
endmodule

