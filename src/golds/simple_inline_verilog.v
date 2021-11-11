module simple_inline_verilog_inline_verilog_0(
  input I);

  // This is a comment.	// <stdin>:3:5
endmodule

module simple_inline_verilog(
  input  I,
  output O);

  simple_inline_verilog_inline_verilog_0 simple_inline_verilog_inline_verilog_inst_0 (	// <stdin>:8:5
    .I (1'h0)	// <stdin>:7:14
  );
  assign O = I;	// <stdin>:9:5
endmodule

