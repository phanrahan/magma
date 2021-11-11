module simple_mixed_direction_ports(
  input  [7:0] simple_mixed_direction_ports_a_x,
  output [7:0] simple_mixed_direction_ports_a_y);

  assign simple_mixed_direction_ports_a_y = simple_mixed_direction_ports_a_x;	// <stdin>:3:5
endmodule

module complex_mixed_direction_ports2(
  input  [7:0] complex_mixed_direction_ports2_a_x,
  output [7:0] complex_mixed_direction_ports2_a_y);

  simple_mixed_direction_ports simple_mixed_direction_ports_inst0 (	// <stdin>:6:76
    .simple_mixed_direction_ports_a_x (complex_mixed_direction_ports2_a_x),
    .simple_mixed_direction_ports_a_y (complex_mixed_direction_ports2_a_y)
  );
endmodule

