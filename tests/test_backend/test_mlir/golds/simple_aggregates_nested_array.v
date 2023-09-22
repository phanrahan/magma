module simple_aggregates_nested_array(
  input  [7:0][3:0][15:0] a,
  output [7:0][3:0][15:0] y
);

  assign y = {a[3'h0 +: 4], a[3'h4 +: 4]};
endmodule

