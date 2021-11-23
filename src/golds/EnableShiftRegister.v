module EnableShiftRegister(	// <stdin>:1:1
  input  [3:0] I,
  input        shift, CLK, ASYNCRESET,
  output [3:0] O);

  reg [3:0] Register_inst0;	// <stdin>:2:10
  reg [3:0] Register_inst1;	// <stdin>:13:10
  reg [3:0] Register_inst2;	// <stdin>:23:10
  reg [3:0] Register_inst3;	// <stdin>:33:10

  always_ff @(posedge shift or posedge CLK) begin	// <stdin>:34:5
    if (CLK) begin	// <stdin>:34:5
      Register_inst0 <= 4'h0;	// <stdin>:6:9, :8:10
      Register_inst1 <= 4'h0;	// <stdin>:8:10, :17:9
      Register_inst2 <= 4'h0;	// <stdin>:8:10, :27:9
      Register_inst3 <= 4'h0;	// <stdin>:8:10, :37:9
    end
    else begin	// <stdin>:34:5
      Register_inst0 <= I;	// <stdin>:4:9
      Register_inst1 <= Register_inst0;	// <stdin>:12:10, :15:9
      Register_inst2 <= Register_inst1;	// <stdin>:22:10, :25:9
      Register_inst3 <= Register_inst2;	// <stdin>:32:10, :35:9
    end
  end // always_ff @(posedge or posedge)
  initial begin	// <stdin>:39:5
    Register_inst0 = 4'h0;	// <stdin>:8:10, :10:9
    Register_inst1 = 4'h0;	// <stdin>:8:10, :20:9
    Register_inst2 = 4'h0;	// <stdin>:8:10, :30:9
    Register_inst3 = 4'h0;	// <stdin>:8:10, :40:9
  end // initial
  assign O = Register_inst3;	// <stdin>:42:10, :43:5
endmodule

