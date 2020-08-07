// Module `Foo` defined externally
module Main (
    input z_0_x,
    output z_0_y,
    input z_1_x,
    output z_1_y
);
wire Foo_inst0_z_0_x;
wire Foo_inst0_z_0_y;
wire Foo_inst0_z_1_x;
wire a_x;
wire a_y;
assign Foo_inst0_z_0_x = a_y;
assign Foo_inst0_z_1_x = z_0_x;
Foo Foo_inst0 (
    .z_0_x(Foo_inst0_z_0_x),
    .z_0_y(Foo_inst0_z_0_y),
    .z_1_x(Foo_inst0_z_1_x),
    .z_1_y(z_1_y)
);
assign a_x = Foo_inst0_z_0_y;
assign a_y = z_0_x;
assign z_0_y = a_x;
endmodule

