module simple_comb(
  input  [15:0] a,
                b,
                c,
  output [15:0] y,
                z
);

  assign y = 16'hFFFF;
  assign z = 16'hFFFF;
endmodule

module simple_unused_output(
  input  [15:0] a,
                b,
                c,
  output [15:0] y
);

  simple_comb simple_comb_inst0 (
    .a (a),
    .b (b),
    .c (c),
    .y (/* unused */),
    .z (y)
  );
endmodule

