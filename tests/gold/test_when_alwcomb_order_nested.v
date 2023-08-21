// Generated by CIRCT firtool-1.48.0-34-g7018fb13b
module test_when_alwcomb_order(
  input  struct packed {logic x; logic [7:0] y; } I,
  input                                           S,
  output struct packed {logic x; logic [7:0] y; } O
);

  reg                                          _GEN;
  always_comb begin
    if (S)
      _GEN = I.x;
    else
      _GEN = ~I.x;
  end // always_comb
  reg [7:0]                                    _GEN_0;
  always_comb begin
    if (S)
      _GEN_0 = I.y;
    else
      _GEN_0 = ~I.y;
  end // always_comb
     struct packed {logic x; logic [7:0] y; } _GEN_1;
  always_comb begin
    _GEN_1 = I;
    if (S)
      _GEN_1 = '{x: _GEN, y: _GEN_0};
  end // always_comb
  assign O = _GEN_1;
endmodule

