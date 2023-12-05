module DebugModule(
  input port_0,
        port_1,
        port_2
);

  reg reg_0;
  always_ff @(posedge port_0)
    reg_0 <= reg_0 | port_1;
  initial
    reg_0 = 1'h0;
  assert port_2;
  assert ~reg_0;
endmodule

module Top(
  input  I,
         CLK,
  output O
);

  `ifdef DEBUG
    DebugModule DebugModule (
      .port_0 (CLK),
      .port_1 (I),
      .port_2 (I)
    );
  `endif // DEBUG
  assign O = I;
endmodule

