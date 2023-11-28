module simple_disallow_local_variables(
  input  [1:0] x,
  input        s,
  output [1:0] O
);

  reg [1:0] _GEN;
  always_comb begin
    if (s) begin
      automatic logic [1:0] _GEN_0 = ~x;
      _GEN = {_GEN_0[1], _GEN_0[0]};
    end
    else
      _GEN = {x[1], x[0]};
  end // always_comb
  reg       _GEN_1;
  reg       _GEN_2;
  always_comb begin
    if (~s) begin
      _GEN_1 = _GEN[1];
      _GEN_2 = _GEN[0];
    end
    else begin
      _GEN_1 = _GEN[0];
      _GEN_2 = _GEN[1];
    end
  end // always_comb
  assign O = {_GEN_2, _GEN_1};
endmodule

