module simple_comb(	// <stdin>:1:1
  input  [15:0] a, b, c,
  output [15:0] y, z);

  assign y = 16'hFFFF;	// <stdin>:2:10, :6:5
  assign z = 16'hFFFF;	// <stdin>:2:10, :6:5
endmodule

module simple_undriven_instances();	// <stdin>:8:1
  wire [15:0] simple_comb_inst1_y;	// <stdin>:22:16
  wire [15:0] simple_comb_inst1_z;	// <stdin>:22:16
  wire [15:0] simple_comb_inst0_y;	// <stdin>:15:14
  wire [15:0] simple_comb_inst0_z;	// <stdin>:15:14
  wire [15:0] _T;	// <stdin>:9:10
  wire [15:0] _T_0;	// <stdin>:11:10
  wire [15:0] _T_1;	// <stdin>:13:10
  wire [15:0] _T_2;	// <stdin>:16:10
  wire [15:0] _T_3;	// <stdin>:18:11
  wire [15:0] _T_4;	// <stdin>:20:11

  simple_comb simple_comb_inst0 (	// <stdin>:15:14
    .a (_T),	// <stdin>:10:10
    .b (_T_0),	// <stdin>:12:10
    .c (_T_1),	// <stdin>:14:10
    .y (simple_comb_inst0_y),
    .z (simple_comb_inst0_z)
  );
  simple_comb simple_comb_inst1 (	// <stdin>:22:16
    .a (_T_2),	// <stdin>:17:10
    .b (_T_3),	// <stdin>:19:11
    .c (_T_4),	// <stdin>:21:11
    .y (simple_comb_inst1_y),
    .z (simple_comb_inst1_z)
  );
endmodule

