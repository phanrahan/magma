module ShiftRegister(
  input  I, CLK,
  output O);

  reg Register_inst0;	// <stdin>:3:23
  reg Register_inst1;	// <stdin>:4:23
  reg Register_inst2;	// <stdin>:5:23
  reg Register_inst3;	// <stdin>:6:23

  always @(posedge CLK) begin	// <stdin>:7:5
    Register_inst0 <= I;	// <stdin>:11:7
    Register_inst1 <= Register_inst0;	// <stdin>:10:12, :12:7
    Register_inst2 <= Register_inst1;	// <stdin>:9:12, :13:7
    Register_inst3 <= Register_inst2;	// <stdin>:8:12, :14:7
  end // always @(posedge)
  initial begin	// <stdin>:16:5
    Register_inst0 = 1'h0;	// <stdin>:17:16, :18:7
    Register_inst1 = 1'h0;	// <stdin>:17:16, :19:7
    Register_inst2 = 1'h0;	// <stdin>:17:16, :20:7
    Register_inst3 = 1'h0;	// <stdin>:17:16, :21:7
  end // initial
  assign O = Register_inst3;	// <stdin>:23:10, :24:5
endmodule

