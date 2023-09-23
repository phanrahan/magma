module test_when_alwcomb_order_nested_2(
  input  struct packed {logic x; logic [7:0] y; }[2:0] I,
  input                                                S,
  output struct packed {logic x; logic [7:0] y; }      O
);

  reg       _GEN;
  always_comb begin
    if (S)
      _GEN = I[2'h1].x;
    else
      _GEN = I[2'h2].x;
  end // always_comb
  reg [7:0] _GEN_0;
  always_comb begin
    if (S)
      _GEN_0 = I[2'h1].y;
    else
      _GEN_0 = I[2'h2].y;
  end // always_comb
  reg       _GEN_1;
  reg [7:0] _GEN_2;
  always_comb begin
    _GEN_1 = I[2'h0].x;
    _GEN_2 = I[2'h0].y;
    if (S) begin
    end
    else begin
      _GEN_1 = _GEN;
      _GEN_2 = _GEN_0;
    end
  end // always_comb
  assign O = '{x: _GEN_1, y: _GEN_2};
endmodule

