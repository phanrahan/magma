module simple_mixed_direction_ports(
  input  [7:0] simple_mixed_direction_ports_a_x,
  output [7:0] simple_mixed_direction_ports_a_y);

  assign simple_mixed_direction_ports_a_y = simple_mixed_direction_ports_a_x;	// <stdin>:3:5
endmodule

