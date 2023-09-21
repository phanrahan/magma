// external module simple_verilog_defn

module simple_verilog_defn_wrapper(
  input  I,
  output O
);

  simple_verilog_defn simple_verilog_defn_inst0 (
    .I (I),
    .O (O)
  );
endmodule

