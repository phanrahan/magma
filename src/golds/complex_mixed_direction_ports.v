module complex_mixed_direction_ports(
  input  [7:0] complex_mixed_direction_ports_a_0_x, complex_mixed_direction_ports_a_1_x,
  input  [7:0] complex_mixed_direction_ports_a_2_x, complex_mixed_direction_ports_a_3_x,
  input  [7:0] complex_mixed_direction_ports_a_4_x, complex_mixed_direction_ports_a_5_x,
  input  [7:0] complex_mixed_direction_ports_a_6_x, complex_mixed_direction_ports_a_7_x,
  input  [7:0] complex_mixed_direction_ports_b_y,
  output [7:0] complex_mixed_direction_ports_a_0_y, complex_mixed_direction_ports_a_1_y,
  output [7:0] complex_mixed_direction_ports_a_2_y, complex_mixed_direction_ports_a_3_y,
  output [7:0] complex_mixed_direction_ports_a_4_y, complex_mixed_direction_ports_a_5_y,
  output [7:0] complex_mixed_direction_ports_a_6_y, complex_mixed_direction_ports_a_7_y,
  output [7:0] complex_mixed_direction_ports_b_x);

  assign complex_mixed_direction_ports_a_0_y = 8'h0;	// <stdin>:3:14, :4:5
  assign complex_mixed_direction_ports_a_1_y = complex_mixed_direction_ports_b_y;	// <stdin>:4:5
  assign complex_mixed_direction_ports_a_2_y = 8'h0;	// <stdin>:3:14, :4:5
  assign complex_mixed_direction_ports_a_3_y = 8'h0;	// <stdin>:3:14, :4:5
  assign complex_mixed_direction_ports_a_4_y = 8'h0;	// <stdin>:3:14, :4:5
  assign complex_mixed_direction_ports_a_5_y = 8'h0;	// <stdin>:3:14, :4:5
  assign complex_mixed_direction_ports_a_6_y = 8'h0;	// <stdin>:3:14, :4:5
  assign complex_mixed_direction_ports_a_7_y = 8'h0;	// <stdin>:3:14, :4:5
  assign complex_mixed_direction_ports_b_x = complex_mixed_direction_ports_a_1_x;	// <stdin>:4:5
endmodule

