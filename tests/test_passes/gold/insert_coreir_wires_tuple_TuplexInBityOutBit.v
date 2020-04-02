// Module `Foo` defined externally
module Main (
    input z_x,
    output z_y
);
wire Foo_inst0_z_y;
wire a_x;
wire a_y;
Foo Foo_inst0 (
    .z_x(a_y),
    .z_y(Foo_inst0_z_y)
);
assign a_x = Foo_inst0_z_y;
assign a_y = z_x;
assign z_y = a_x;
endmodule

