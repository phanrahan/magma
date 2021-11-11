module EnableShiftRegister(
  input  [3:0] I,
  input        shift, CLK, ASYNCRESET,
  output [3:0] O);

  reg [3:0] Register_inst0;	// <stdin>:3:23
  reg [3:0] Register_inst1;	// <stdin>:4:23
  reg [3:0] Register_inst2;	// <stdin>:5:23
  reg [3:0] Register_inst3;	// <stdin>:6:23

  always @(posedge shift or posedge CLK) begin	// <stdin>:7:5
    if (CLK) begin	// <stdin>:7:5
      Register_inst0 <= 4'h0;	// <stdin>:16:16, :17:7
      Register_inst1 <= 4'h0;	// <stdin>:16:16, :18:7
      Register_inst2 <= 4'h0;	// <stdin>:16:16, :19:7
      Register_inst3 <= 4'h0;	// <stdin>:16:16, :20:7
    end
    else begin	// <stdin>:7:5
      Register_inst0 <= I;	// <stdin>:11:7
      Register_inst1 <= Register_inst0;	// <stdin>:10:12, :12:7
      Register_inst2 <= Register_inst1;	// <stdin>:9:12, :13:7
      Register_inst3 <= Register_inst2;	// <stdin>:8:12, :14:7
    end
  end // always @(posedge or posedge)
  initial begin	// <stdin>:22:5
    Register_inst0 = 4'h0;	// <stdin>:23:16, :24:7
    Register_inst1 = 4'h0;	// <stdin>:23:16, :25:7
    Register_inst2 = 4'h0;	// <stdin>:23:16, :26:7
    Register_inst3 = 4'h0;	// <stdin>:23:16, :27:7
  end // initial
  assign O = Register_inst3;	// <stdin>:29:10, :30:5
endmodule

