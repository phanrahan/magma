// Module `Foo` defined externally
module Main (
    input z_0_x,
    output z_0_y,
    input z_1_x,
    output z_1_y
);
wire a_x;
wire a_y;
wire foo_z_0_y;
assign a_x = foo_z_0_y;
assign a_y = z_0_x;
Foo foo (
    .z_0_x(a_y),
    .z_0_y(foo_z_0_y),
    .z_1_x(z_0_x),
    .z_1_y(z_1_y)
);
assign z_0_y = a_x;
endmodule

