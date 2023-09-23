module test_when_alwcomb_order(
  input  [7:0] I,
  input        S,
  output [7:0] O
);

  reg [7:0] _GEN;
  always_comb begin
    if (S)
      _GEN = I;
    else
      _GEN = ~I;
  end // always_comb
  reg [7:0] _GEN_0;
  always_comb begin
    _GEN_0 = _GEN;
    if (S) begin
    end
    else
      _GEN_0 = ~_GEN;
  end // always_comb
  assign O = _GEN_0;
endmodule

