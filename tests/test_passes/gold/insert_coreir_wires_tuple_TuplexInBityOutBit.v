// Module `Foo` defined externally
module Main (
    input z_x,
    output z_y
);
wire Foo_inst0_z_y;
wire [1:0] a;
Foo Foo_inst0 (
    .z_x(a[1]),
    .z_y(Foo_inst0_z_y)
);
assign a = {z_x,Foo_inst0_z_y};
assign z_y = a[0];
endmodule

