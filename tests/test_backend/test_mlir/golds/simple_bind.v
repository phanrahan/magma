module simple_bind_asserts(
  input I,
        O,
        CLK
);

  assert property (@(posedge CLK) I |-> ##1 O);
endmodule

module simple_bind(
  input  I,
         CLK,
  output O
);

  reg Register_inst0;
  always_ff @(posedge CLK)
    Register_inst0 <= I;
  initial
    Register_inst0 = 1'h0;
  assign O = Register_inst0;
endmodule


// ----- 8< ----- FILE "bindfile.sv" ----- 8< -----

bind simple_bind simple_bind_asserts simple_bind_asserts_inst0 (
  .I   (I),
  .O   (Register_inst0),
  .CLK (CLK)
);
