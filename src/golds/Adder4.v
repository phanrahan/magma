module FullAdder(
  input  a, b, cin,
  output sum_, cout);

  assign sum_ = a ^ b ^ cin;	// <stdin>:3:10, :8:5
  assign cout = a & b | b & cin | a & cin;	// <stdin>:4:10, :5:10, :6:10, :7:10, :8:5
endmodule

module Adder4(
  input  [3:0] A, B,
  input        CIN,
  output [3:0] SUM,
  output       COUT);

  wire FullAdder_inst3_sum_;	// <stdin>:22:52
  wire FullAdder_inst2_sum_;	// <stdin>:19:52
  wire FullAdder_inst2_cout;	// <stdin>:19:52
  wire FullAdder_inst1_sum_;	// <stdin>:16:52
  wire FullAdder_inst1_cout;	// <stdin>:16:52
  wire FullAdder_inst0_sum_;	// <stdin>:13:52
  wire FullAdder_inst0_cout;	// <stdin>:13:52

  FullAdder FullAdder_inst0 (	// <stdin>:13:52
    .a    (A[0]),	// <stdin>:11:10
    .b    (B[0]),	// <stdin>:12:10
    .cin  (CIN),
    .sum_ (FullAdder_inst0_sum_),
    .cout (FullAdder_inst0_cout)
  );
  FullAdder FullAdder_inst1 (	// <stdin>:16:52
    .a    (A[1]),	// <stdin>:14:10
    .b    (B[1]),	// <stdin>:15:10
    .cin  (FullAdder_inst0_cout),	// <stdin>:13:52
    .sum_ (FullAdder_inst1_sum_),
    .cout (FullAdder_inst1_cout)
  );
  FullAdder FullAdder_inst2 (	// <stdin>:19:52
    .a    (A[2]),	// <stdin>:17:10
    .b    (B[2]),	// <stdin>:18:10
    .cin  (FullAdder_inst1_cout),	// <stdin>:16:52
    .sum_ (FullAdder_inst2_sum_),
    .cout (FullAdder_inst2_cout)
  );
  FullAdder FullAdder_inst3 (	// <stdin>:22:52
    .a    (A[3]),	// <stdin>:20:10
    .b    (B[3]),	// <stdin>:21:10
    .cin  (FullAdder_inst2_cout),	// <stdin>:19:52
    .sum_ (FullAdder_inst3_sum_),
    .cout (COUT)
  );
  assign SUM = {FullAdder_inst3_sum_, FullAdder_inst2_sum_, FullAdder_inst1_sum_, FullAdder_inst0_sum_};	// <stdin>:13:52, :16:52, :19:52, :22:52, :23:10, :24:5
endmodule

