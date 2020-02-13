// Module `Foo` defined externally
module corebit_wire (input in, output out);
  assign out = in;
endmodule

module Main (input z_0_x, output z_0_y, input z_1_x, output z_1_y);
wire Foo_inst0_z_0_y;
wire Foo_inst0_z_1_y;
wire a_x_out;
wire a_y_out;
Foo Foo_inst0(.z_0_x(a_y_out), .z_0_y(Foo_inst0_z_0_y), .z_1_x(z_0_x), .z_1_y(Foo_inst0_z_1_y));
corebit_wire a_x(.in(Foo_inst0_z_0_y), .out(a_x_out));
corebit_wire a_y(.in(z_0_x), .out(a_y_out));
assign z_0_y = a_x_out;
assign z_1_y = Foo_inst0_z_1_y;
endmodule

