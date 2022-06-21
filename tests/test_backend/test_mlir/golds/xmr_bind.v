module xmr_bind_grandchild(	// <stdin>:1:1
  input  [15:0] a,
  output [15:0] y);

  assign y = a;	// <stdin>:2:5
endmodule

module xmr_bind_child(	// <stdin>:4:1
  input  [15:0] a,
  output [15:0] y);

  xmr_bind_grandchild xmr_bind_grandchild_inst0 (	// <stdin>:5:10
    .a (a),
    .y (y)
  );
endmodule

module xmr_bind_asserts(	// <stdin>:8:1
  input [15:0] a, y, other, that);

  wire [15:0] _magma_inline_wire0;	// <stdin>:9:10
  wire [15:0] _magma_inline_wire1;	// <stdin>:12:10

  assign _magma_inline_wire0 = other;	// <stdin>:10:5
  assign _magma_inline_wire1 = that;	// <stdin>:13:5
  assert property (_magma_inline_wire0 == 0 && _magma_inline_wire1 == 0);	// <stdin>:11:10, :14:10, :15:5
endmodule

module xmr_bind(	// <stdin>:17:1
  input  [15:0] a,
  output [15:0] y);

  wire [15:0] xmr_bind_asserts_inst_other;	// <stdin>:23:5
  wire [15:0] xmr_bind_asserts_inst_that;	// <stdin>:23:5
  wire [15:0] xmr_bind_child_inst0_y;	// <stdin>:18:10

  xmr_bind_child xmr_bind_child_inst0 (	// <stdin>:18:10
    .a (a),
    .y (xmr_bind_child_inst0_y)
  );
  assign xmr_bind_asserts_inst_other = xmr_bind_child_inst0.xmr_bind_grandchild_inst0.y;	// <stdin>:19:10, :20:10, :23:5
  assign xmr_bind_asserts_inst_that = my_value;	// <stdin>:21:10, :22:10, :23:5
  /* This instance is elsewhere emitted as a bind statement.
    xmr_bind_asserts xmr_bind_asserts_inst (	// <stdin>:23:5
      .a     (a),
      .y     (xmr_bind_child_inst0_y),	// <stdin>:18:10
      .other (xmr_bind_asserts_inst_other),	// <stdin>:23:5
      .that  (xmr_bind_asserts_inst_that)	// <stdin>:23:5
    );
  */
  assign y = xmr_bind_child_inst0_y;	// <stdin>:18:10, :24:5
endmodule


// ----- 8< ----- FILE "bindfile" ----- 8< -----

bind xmr_bind xmr_bind_asserts xmr_bind_asserts_inst (
  .a     (a),
  .y     (xmr_bind_child_inst0_y),
  .other (xmr_bind_asserts_inst_other),
  .that  (xmr_bind_asserts_inst_that)
);
