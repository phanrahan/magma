module complex_inline_verilog(	// <stdin>:1:1
  input  I, CLK,
  output O);

  reg  Register_inst0;	// <stdin>:2:10
  wire _magma_inline_wire0;	// <stdin>:11:10
  wire _magma_inline_wire1;	// <stdin>:14:10

  always_ff @(posedge CLK)	// <stdin>:3:5
    Register_inst0 <= I;	// <stdin>:4:9
  initial	// <stdin>:7:5
    Register_inst0 = 1'h0;	// <stdin>:6:10, :8:9
  assign _magma_inline_wire0 = Register_inst0;	// <stdin>:10:10, :12:5
  assign _magma_inline_wire1 = I;	// <stdin>:15:5
  assert property (@(posedge CLK) _magma_inline_wire1 |-> ##1 _magma_inline_wire0);	// <stdin>:13:10, :16:10, :17:5
  assign O = Register_inst0;	// <stdin>:10:10, :18:5
endmodule

