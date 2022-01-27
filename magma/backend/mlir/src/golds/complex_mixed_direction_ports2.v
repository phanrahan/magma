module simple_mixed_direction_ports(	// <stdin>:1:1
  input  [7:0] a_x,
  output [7:0] a_y);

  assign a_y = a_x;	// <stdin>:2:5
endmodule

module complex_mixed_direction_ports2(	// <stdin>:4:1
  input  [7:0] a_x,
  output [7:0] a_y);

  simple_mixed_direction_ports simple_mixed_direction_ports_inst0 (	// <stdin>:5:10
    .a_x (a_x),
    .a_y (a_y)
  );
endmodule

