// Generated by CIRCT circtorg-0.0.0-1773-g7abbc4313
module simple_array_of_bit(
  input  [7:0] I,
  output [7:0] O
);

  assign O = {I[0], I[1], I[2], I[3], I[4], I[5], I[6], I[7]};
endmodule

