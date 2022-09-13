module COND1_compile_guard(	// <stdin>:1:1
  input port_0, CLK);

  reg Register_inst0;	// <stdin>:2:10

  always_ff @(posedge CLK)	// <stdin>:3:5
    Register_inst0 <= port_0;	// <stdin>:4:9
  initial	// <stdin>:7:5
    Register_inst0 = 1'h0;	// <stdin>:6:10, :8:9
endmodule

module COND2_compile_guard(	// <stdin>:12:1
  input port_0, CLK);

  reg Register_inst0;	// <stdin>:13:10

  always_ff @(posedge CLK)	// <stdin>:14:5
    Register_inst0 <= port_0;	// <stdin>:15:9
  initial	// <stdin>:18:5
    Register_inst0 = 1'h0;	// <stdin>:17:10, :19:9
endmodule

module simple_compile_guard(	// <stdin>:23:1
  input  I, CLK,
  output O);

  `ifdef COND1	// <stdin>:24:5
    COND1_compile_guard COND1_compile_guard (	// <stdin>:25:9
      .port_0 (I),
      .CLK    (CLK)
    );
  `endif
  `ifndef COND2	// <stdin>:27:5
    COND2_compile_guard COND2_compile_guard (	// <stdin>:29:9
      .port_0 (I),
      .CLK    (CLK)
    );
  `endif
  assign O = I;	// <stdin>:31:5
endmodule

