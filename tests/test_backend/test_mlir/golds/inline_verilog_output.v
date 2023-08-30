module inline_verilog_output(
  input  I,
         CLK,
  output O
);

  reg Register_inst0;
  always_ff @(posedge CLK)
    Register_inst0 <= I;
  initial
    Register_inst0 = 1'h0;
  assert property (@(posedge CLK) I |-> ##1 Register_inst0);
  assign O = Register_inst0;
endmodule

