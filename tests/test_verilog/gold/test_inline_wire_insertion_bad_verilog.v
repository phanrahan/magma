module test_wire_insertion_bad_verilog(
  input  [31:0] I,
  output        O
);

  `ifdef LOGGING_ON
  $display("%x", I[0]);
  `endif LOGGING_ON
  assign O = I[0];
endmodule

