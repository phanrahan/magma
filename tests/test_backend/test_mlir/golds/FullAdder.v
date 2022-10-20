module FullAdder(
  input  a, b, cin,
  output sum_, cout);

  assign sum_ = a ^ b ^ cin;
  assign cout = a & b | b & cin | a & cin;
endmodule

