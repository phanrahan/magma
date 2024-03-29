module simple_aggregates_array(
  input  [7:0][15:0] a,
  output [7:0][15:0] y,
  output [3:0][15:0] z
);

  wire [3:0][15:0] _GEN = a[3'h0 +: 4];
  assign y = {_GEN, a[3'h4 +: 4]};
  assign z = _GEN;
endmodule

