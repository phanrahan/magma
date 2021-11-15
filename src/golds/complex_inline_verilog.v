module complex_inline_verilog(
  input  I, CLK,
  output O);

  reg  Register_inst0;	// <stdin>:3:23
  wire _magma_inline_wire0;	// <stdin>:12:28
  wire _magma_inline_wire1;	// <stdin>:15:28

  always @(posedge CLK)	// <stdin>:4:5
    Register_inst0 <= I;	// <stdin>:5:7
  initial	// <stdin>:7:5
    Register_inst0 = 1'h0;	// <stdin>:8:16, :9:7
  wire _T = Register_inst0;	// <stdin>:11:10
  assign _magma_inline_wire0 = _T;	// <stdin>:13:5
  assign _magma_inline_wire1 = I;	// <stdin>:16:5
  assert property (@(posedge CLK) _magma_inline_wire1 |-> ##1 _magma_inline_wire0);	// <stdin>:14:10, :17:10, :18:5
  assign O = _T;	// <stdin>:19:5
endmodule

