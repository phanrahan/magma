module FullAdder(
  input  a, b, cin,
  output sum_, cout);

  assign sum_ = a ^ b ^ cin;
  assign cout = a & b | b & cin | a & cin;
endmodule

module Adder4(
  input  [3:0] A, B,
  input        CIN,
  output [3:0] SUM,
  output       COUT);

  wire FullAdder_inst3_sum_;
  wire FullAdder_inst2_sum_;
  wire FullAdder_inst2_cout;
  wire FullAdder_inst1_sum_;
  wire FullAdder_inst1_cout;
  wire FullAdder_inst0_sum_;
  wire FullAdder_inst0_cout;

  FullAdder FullAdder_inst0 (
    .a    (A[0]),
    .b    (B[0]),
    .cin  (CIN),
    .sum_ (FullAdder_inst0_sum_),
    .cout (FullAdder_inst0_cout)
  );
  FullAdder FullAdder_inst1 (
    .a    (A[1]),
    .b    (B[1]),
    .cin  (FullAdder_inst0_cout),
    .sum_ (FullAdder_inst1_sum_),
    .cout (FullAdder_inst1_cout)
  );
  FullAdder FullAdder_inst2 (
    .a    (A[2]),
    .b    (B[2]),
    .cin  (FullAdder_inst1_cout),
    .sum_ (FullAdder_inst2_sum_),
    .cout (FullAdder_inst2_cout)
  );
  FullAdder FullAdder_inst3 (
    .a    (A[3]),
    .b    (B[3]),
    .cin  (FullAdder_inst2_cout),
    .sum_ (FullAdder_inst3_sum_),
    .cout (COUT)
  );
  assign SUM = {FullAdder_inst3_sum_, FullAdder_inst2_sum_, FullAdder_inst1_sum_, FullAdder_inst0_sum_};
endmodule

