module twizzler(	// <stdin>:1:1
  input  I0, I1, I2,
  output O0, O1, O2);

  assign O0 = ~I1;	// <stdin>:3:10, :6:5
  assign O1 = ~I0;	// <stdin>:4:10, :6:5
  assign O2 = ~I2;	// <stdin>:5:10, :6:5
endmodule

module twizzle(	// <stdin>:8:1
  input  I,
  output O);

  wire t1_O0;	// <stdin>:10:18
  wire t1_O1;	// <stdin>:10:18
  wire t0_O0;	// <stdin>:9:18
  wire t0_O1;	// <stdin>:9:18
  wire t0_O2;	// <stdin>:9:18

  twizzler t0 (	// <stdin>:9:18
    .I0 (I),
    .I1 (t1_O0),	// <stdin>:10:18
    .I2 (t1_O1),	// <stdin>:10:18
    .O0 (t0_O0),
    .O1 (t0_O1),
    .O2 (t0_O2)
  );
  twizzler t1 (	// <stdin>:10:18
    .I0 (t0_O0),	// <stdin>:9:18
    .I1 (t0_O1),	// <stdin>:9:18
    .I2 (t0_O2),	// <stdin>:9:18
    .O0 (t1_O0),
    .O1 (t1_O1),
    .O2 (O)
  );
endmodule

