module complex_undriven(
  output struct packed {logic [7:0] x; logic y; } O
);

  wire [7:0] _GEN;
  wire       _GEN_0;
  assign O = '{x: _GEN, y: _GEN_0};
endmodule

