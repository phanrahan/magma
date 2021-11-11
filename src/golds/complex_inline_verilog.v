module complex_inline_verilog_inline_verilog_0(
  input __magma_inline_value_0, __magma_inline_value_1);

  assert property (@(posedge CLK) __magma_inline_value_1 |-> ##1 __magma_inline_value_0);	// <stdin>:3:5
endmodule

module complex_inline_verilog(
  input  I, CLK,
  output O);

  reg  Register_inst0;	// <stdin>:7:23
  wire _magma_inline_wire0;	// <stdin>:16:28
  wire _magma_inline_wire1;	// <stdin>:19:28

  always @(posedge CLK)	// <stdin>:8:5
    Register_inst0 <= I;	// <stdin>:9:7
  initial	// <stdin>:11:5
    Register_inst0 = 1'h0;	// <stdin>:12:16, :13:7
  wire _T = Register_inst0;	// <stdin>:15:10
  assign _magma_inline_wire0 = _T;	// <stdin>:17:5
  assign _magma_inline_wire1 = I;	// <stdin>:20:5
  complex_inline_verilog_inline_verilog_0 complex_inline_verilog_inline_verilog_inst_0 (	// <stdin>:22:5
    .__magma_inline_value_0 (_magma_inline_wire0),	// <stdin>:18:10
    .__magma_inline_value_1 (_magma_inline_wire1)	// <stdin>:21:10
  );
  assign O = _T;	// <stdin>:23:5
endmodule

