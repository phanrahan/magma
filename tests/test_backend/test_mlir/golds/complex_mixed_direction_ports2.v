module simple_mixed_direction_ports(
  input  [7:0] a_x,
  output [7:0] a_y
);

  assign a_y = a_x;
endmodule

module complex_mixed_direction_ports2(
  input  [7:0] a_x,
  output [7:0] a_y
);

  simple_mixed_direction_ports simple_mixed_direction_ports_inst0 (
    .a_x (a_x),
    .a_y (a_y)
  );
endmodule

