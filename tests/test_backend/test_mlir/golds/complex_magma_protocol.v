module simple_magma_protocol(
  input  [7:0] I,
  output [7:0] O
);

  assign O = I;
endmodule

module complex_magma_protocol(
  input  [7:0] I,
  output [7:0] O
);

  simple_magma_protocol simple_magma_protocol_inst0 (
    .I (I),
    .O (O)
  );
endmodule

