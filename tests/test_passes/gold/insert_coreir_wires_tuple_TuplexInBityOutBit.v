// Module `Foo` defined externally
module corebit_wire (
    input in,
    output out
);
  assign out = in;
endmodule

module Main (
    input z_x,
    output z_y
);
wire Foo_inst0_z_y;
wire a_x_out;
wire a_y_out;
Foo Foo_inst0 (
    .z_x(a_y_out),
    .z_y(Foo_inst0_z_y)
);
corebit_wire a_x (
    .in(Foo_inst0_z_y),
    .out(a_x_out)
);
corebit_wire a_y (
    .in(z_x),
    .out(a_y_out)
);
assign z_y = a_x_out;
endmodule

