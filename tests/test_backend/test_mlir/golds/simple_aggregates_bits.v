module simple_aggregates_bits(
  input  [15:0] a,
  output [15:0] y,
  output [7:0]  z
);

  assign y = {a[7:0], a[15:8]};
  assign z = a[7:0];
endmodule

