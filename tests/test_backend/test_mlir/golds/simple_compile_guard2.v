module simple_compile_guard2(	// <stdin>:1:1
  input  I, CLK,
  output O);

  `ifdef COND1	// <stdin>:2:5
    reg Register_inst0;	// <stdin>:3:14

    always_ff @(posedge CLK)	// <stdin>:4:9
      Register_inst0 <= I;	// <stdin>:5:13
    initial	// <stdin>:7:9
      Register_inst0 = 1'h0;	// <stdin>:8:13, :12:10
  `endif
  `ifdef COND2	// <stdin>:13:5
    reg Register_inst1;	// <stdin>:14:14

    always_ff @(posedge CLK)	// <stdin>:15:9
      Register_inst1 <= I;	// <stdin>:16:13
    initial	// <stdin>:18:9
      Register_inst1 = 1'h0;	// <stdin>:12:10, :19:13
  `endif
  assign O = I;	// <stdin>:23:5
endmodule

