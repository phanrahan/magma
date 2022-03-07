module simple_shifts(	// <stdin>:1:1
  input  [7:0] I00, I01, I10, I11, I20, I21,
  output [7:0] O0, O1, O2);

  assign O0 = I00 << I01;	// <stdin>:2:10, :5:5
  assign O1 = I10 >> I11;	// <stdin>:3:10, :5:5
  assign O2 = $signed($signed(I20) >>> I21);	// <stdin>:4:10, :5:5
endmodule

