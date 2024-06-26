module complex_wire(
  input  [7:0]      I0,
  input             I1,
  input  [3:0][7:0] I2,
  output [7:0]      O0,
  output            O1,
  output [3:0][7:0] O2
);

  wire [7:0]      tmp0 = I0;
  wire            tmp1 = I1;
  wire [3:0][7:0] tmp2 = I2;
  assign O0 = tmp0;
  assign O1 = tmp1;
  assign O2 = tmp2;
endmodule

