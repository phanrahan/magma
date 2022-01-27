module ShiftRegister(	// <stdin>:1:1
  input  I, CLK,
  output O);

  reg Register_inst0;	// <stdin>:2:10
  reg Register_inst1;	// <stdin>:11:10
  reg Register_inst2;	// <stdin>:19:10
  reg Register_inst3;	// <stdin>:27:10

  always_ff @(posedge CLK) begin	// <stdin>:28:5
    Register_inst0 <= I;	// <stdin>:4:9
    Register_inst1 <= Register_inst0;	// <stdin>:10:10, :13:9
    Register_inst2 <= Register_inst1;	// <stdin>:18:10, :21:9
    Register_inst3 <= Register_inst2;	// <stdin>:26:10, :29:9
  end // always_ff @(posedge)
  initial begin	// <stdin>:31:5
    Register_inst0 = 1'h0;	// <stdin>:6:10, :8:9
    Register_inst1 = 1'h0;	// <stdin>:6:10, :16:9
    Register_inst2 = 1'h0;	// <stdin>:6:10, :24:9
    Register_inst3 = 1'h0;	// <stdin>:6:10, :32:9
  end // initial
  assign O = Register_inst3;	// <stdin>:34:10, :35:5
endmodule

