// Generated by CIRCT firtool-1.48.0-34-g7018fb13b
module Bottom(
  input  I,
  output O
);

  assign O = I;
endmodule

module Middle(
  input  I,
  output O
);

  wire _magma_bind_wire_0 = I;
  Bottom bottom (
    .I (I),
    .O (O)
  );
endmodule

module Top(
  input  I,
  output O
);

  Middle middle (
    .I (I),
    .O (O)
  );
endmodule

