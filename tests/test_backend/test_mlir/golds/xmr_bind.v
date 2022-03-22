module simple_comb(	// <stdin>:1:1
  input  [15:0] a, b, c,
  output [15:0] y, z);

  assign y = 16'hFFFF;	// <stdin>:2:10, :6:5
  assign z = 16'hFFFF;	// <stdin>:2:10, :6:5
endmodule

module simple_hierarchy(	// <stdin>:8:1
  input  [15:0] a, b, c,
  output [15:0] y, z);

  simple_comb simple_comb_inst0 (	// <stdin>:9:14
    .a (a),
    .b (b),
    .c (c),
    .y (y),
    .z (z)
  );
endmodule

module xmr_bind_asserts(	// <stdin>:12:1
  input [15:0] a, b, c, y, z, a_inner);

  wire [15:0] _magma_inline_wire0;	// <stdin>:13:10

  assign _magma_inline_wire0 = a_inner;	// <stdin>:14:5
  assert property (_magma_inline_wire0 == 0);	// <stdin>:15:10, :16:5
endmodule

module xmr_bind(	// <stdin>:18:1
  input  [15:0] a, b, c,
  output [15:0] y, z);

  wire [15:0] xmr_bind_asserts_inst_a_inner;	// <stdin>:22:5
  wire [15:0] inst_y;	// <stdin>:19:14
  wire [15:0] inst_z;	// <stdin>:19:14

  simple_hierarchy inst (	// <stdin>:19:14
    .a (a),
    .b (b),
    .c (c),
    .y (inst_y),
    .z (inst_z)
  );
  assign xmr_bind_asserts_inst_a_inner = inst.simple_comb_inst0.a;	// <stdin>:20:10, :21:10, :22:5
  /* This instance is elsewhere emitted as a bind statement.
    xmr_bind_asserts xmr_bind_asserts_inst (	// <stdin>:22:5
      .a       (a),
      .b       (b),
      .c       (c),
      .y       (inst_y),	// <stdin>:19:14
      .z       (inst_z),	// <stdin>:19:14
      .a_inner (xmr_bind_asserts_inst_a_inner)	// <stdin>:22:5
    );
  */
  assign y = inst_y;	// <stdin>:19:14, :23:5
  assign z = inst_z;	// <stdin>:19:14, :23:5
endmodule


// ----- 8< ----- FILE "bindfile" ----- 8< -----

bind xmr_bind xmr_bind_asserts xmr_bind_asserts_inst (
  .a       (a),
  .b       (b),
  .c       (c),
  .y       (inst_y),
  .z       (inst_z),
  .a_inner (xmr_bind_asserts_inst_a_inner)
);
