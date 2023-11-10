module LUT(
  input  [1:0]                                         I,
  output struct packed {logic [7:0] x; logic y; }[1:0] O
);

  wire [3:0] _GEN = {1'h1, 1'h1, 1'h0, 1'h0};
  wire [3:0] _GEN_0 = {1'h0, 1'h1, 1'h1, 1'h1};
  wire [3:0] _GEN_1 = {1'h0, 1'h1, 1'h1, 1'h0};
  wire [3:0] _GEN_2 = {1'h1, 1'h0, 1'h0, 1'h0};
  wire [3:0] _GEN_3 = {1'h0, 1'h1, 1'h0, 1'h1};
  wire [3:0] _GEN_4 = {1'h1, 1'h0, 1'h1, 1'h1};
  wire [3:0] _GEN_5 = {1'h1, 1'h1, 1'h1, 1'h0};
  wire [3:0] _GEN_6 = {1'h0, 1'h0, 1'h1, 1'h0};
  wire struct packed {logic [7:0] x; logic y; } _GEN_7 =
    '{x: {1'h0, _GEN_1[I], _GEN_6[I], _GEN_2[I], 1'h1, _GEN_4[I], 1'h1, _GEN_0[I]},
      y: _GEN_5[I]};
  wire struct packed {logic [7:0] x; logic y; } _GEN_8 =
    '{x: {_GEN_0[I], _GEN_1[I], 1'h0, _GEN_2[I], _GEN_3[I], 1'h0, _GEN_4[I], _GEN_0[I]},
      y: _GEN[I]};
  assign O = {{_GEN_8}, {_GEN_7}};
endmodule

module complex_lut(
  input  [1:0]                                         a,
  output struct packed {logic [7:0] x; logic y; }[1:0] y
);

  LUT LUT_inst0 (
    .I (a),
    .O (y)
  );
endmodule

