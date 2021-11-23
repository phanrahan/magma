module simple_reduction(	// <stdin>:1:1
  input  [7:0] I0, I1, I2,
  output       O0, O1, O2);

  assign O0 = &I0;	// <stdin>:3:10, :7:5
  assign O1 = |I1;	// <stdin>:5:10, :7:5
  assign O2 = ^I2;	// <stdin>:6:10, :7:5
endmodule

