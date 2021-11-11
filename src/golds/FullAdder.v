module FullAdder(
  input  a, b, cin,
  output sum_, cout);

  assign sum_ = a ^ b ^ cin;	// <stdin>:3:10, :8:5
  assign cout = a & b | b & cin | a & cin;	// <stdin>:4:10, :5:10, :6:10, :7:10, :8:5
endmodule

