module adder3(
  input  [15:0] I0, I1, I2,
  output [15:0] O);

  assign O = I0 + I1 + I2;	// <stdin>:3:10, :4:5
endmodule

