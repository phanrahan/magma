// Module `Foo` defined externally
module Main (
    input z_x,
    output z_y
);
wire a_x;
wire a_y;
wire foo_z_y;
assign a_x = foo_z_y;
assign a_y = z_x;
Foo foo (
    .z_x(a_y),
    .z_y(foo_z_y)
);
assign z_y = a_x;
endmodule

