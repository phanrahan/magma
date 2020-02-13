// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input z_0_x, output z_0_y, input z_1_x, output z_1_y);
wire Foo_inst0_z_0_y;
wire Foo_inst0_z_1_y;
wire [0:0] wire_a_x_z_0_y_out;
wire [0:0] wire_a_y_Foo_inst0_z_0_x_out;
Foo Foo_inst0(.z_0_x(wire_a_y_Foo_inst0_z_0_x_out[0]), .z_0_y(Foo_inst0_z_0_y), .z_1_x(z_0_x), .z_1_y(Foo_inst0_z_1_y));
coreir_wire #(.width(1)) wire_a_x_z_0_y(.in(Foo_inst0_z_0_y), .out(wire_a_x_z_0_y_out));
coreir_wire #(.width(1)) wire_a_y_Foo_inst0_z_0_x(.in(z_0_x), .out(wire_a_y_Foo_inst0_z_0_x_out));
assign z_0_y = wire_a_x_z_0_y_out[0];
assign z_1_y = Foo_inst0_z_1_y;
endmodule

