module simple_array_slice(
  input  [11:0][7:0] a,
  output [3:0][7:0]  y
);

  assign y = a[4'h0 +: 4];
endmodule

