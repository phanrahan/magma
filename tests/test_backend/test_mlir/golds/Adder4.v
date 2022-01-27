module FullAdder(	// <stdin>:1:1
  input  a, b, cin,
  output sum_, cout);

  assign sum_ = a ^ b ^ cin;	// <stdin>:3:10, :9:5
  assign cout = a & b | b & cin | a & cin;	// <stdin>:4:10, :5:10, :7:10, :8:10, :9:5
endmodule

module Adder4(	// <stdin>:11:1
  input  [3:0] A, B,
  input        CIN,
  output [3:0] SUM,
  output       COUT);

  wire FullAdder_inst3_sum_;	// <stdin>:23:16
  wire FullAdder_inst2_sum_;	// <stdin>:20:16
  wire FullAdder_inst2_cout;	// <stdin>:20:16
  wire FullAdder_inst1_sum_;	// <stdin>:17:14
  wire FullAdder_inst1_cout;	// <stdin>:17:14
  wire FullAdder_inst0_sum_;	// <stdin>:14:14
  wire FullAdder_inst0_cout;	// <stdin>:14:14

  FullAdder FullAdder_inst0 (	// <stdin>:14:14
    .a    (A[0]),	// <stdin>:12:10
    .b    (B[0]),	// <stdin>:13:10
    .cin  (CIN),
    .sum_ (FullAdder_inst0_sum_),
    .cout (FullAdder_inst0_cout)
  );
  FullAdder FullAdder_inst1 (	// <stdin>:17:14
    .a    (A[1]),	// <stdin>:15:10
    .b    (B[1]),	// <stdin>:16:10
    .cin  (FullAdder_inst0_cout),	// <stdin>:14:14
    .sum_ (FullAdder_inst1_sum_),
    .cout (FullAdder_inst1_cout)
  );
  FullAdder FullAdder_inst2 (	// <stdin>:20:16
    .a    (A[2]),	// <stdin>:18:10
    .b    (B[2]),	// <stdin>:19:10
    .cin  (FullAdder_inst1_cout),	// <stdin>:17:14
    .sum_ (FullAdder_inst2_sum_),
    .cout (FullAdder_inst2_cout)
  );
  FullAdder FullAdder_inst3 (	// <stdin>:23:16
    .a    (A[3]),	// <stdin>:21:11
    .b    (B[3]),	// <stdin>:22:11
    .cin  (FullAdder_inst2_cout),	// <stdin>:20:16
    .sum_ (FullAdder_inst3_sum_),
    .cout (COUT)
  );
  assign SUM = {FullAdder_inst3_sum_, FullAdder_inst2_sum_, FullAdder_inst1_sum_, FullAdder_inst0_sum_};	// <stdin>:14:14, :17:14, :20:16, :23:16, :24:11, :25:5
endmodule

