module simple_length_one_array(
  input  [0:0][7:0] I,
  output [7:0]      O
);

  assign O = I[1'h0];
endmodule

