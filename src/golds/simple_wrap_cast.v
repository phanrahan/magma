module simple_wrap_cast(	// <stdin>:1:1
  input  I,
  output O);

  wire coreir_wrapInClock_inst0;	// <stdin>:2:10

  assign coreir_wrapInClock_inst0 = I;	// <stdin>:3:5
  assign O = coreir_wrapInClock_inst0;	// <stdin>:4:10, :5:5
endmodule

