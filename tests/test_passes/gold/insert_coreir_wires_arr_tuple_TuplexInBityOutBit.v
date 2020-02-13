// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input z_0_x, output z_0_y, input z_1_x, output z_1_y);
wire Foo_inst0_z_0_y;
wire Foo_inst0_z_1_y;
wire [0:0] wire_Foo_inst0_z_0_y_a_x_out;
wire [0:0] wire_Foo_inst0_z_1_y_z_1_y_out;
wire [0:0] wire_a_x_z_0_y_out;
wire [0:0] wire_a_y_Foo_inst0_z_0_x_out;
wire [0:0] wire_z_0_x_Foo_inst0_z_1_x_out;
wire [0:0] wire_z_0_x_a_y_out;
Foo Foo_inst0(.z_0_x(wire_a_y_Foo_inst0_z_0_x_out[0]), .z_0_y(Foo_inst0_z_0_y), .z_1_x(wire_z_0_x_Foo_inst0_z_1_x_out[0]), .z_1_y(Foo_inst0_z_1_y));
coreir_wire #(.width(1)) wire_Foo_inst0_z_0_y_a_x(.in(Foo_inst0_z_0_y), .out(wire_Foo_inst0_z_0_y_a_x_out));
coreir_wire #(.width(1)) wire_Foo_inst0_z_1_y_z_1_y(.in(Foo_inst0_z_1_y), .out(wire_Foo_inst0_z_1_y_z_1_y_out));
coreir_wire #(.width(1)) wire_a_x_z_0_y(.in(wire_Foo_inst0_z_0_y_a_x_out), .out(wire_a_x_z_0_y_out));
coreir_wire #(.width(1)) wire_a_y_Foo_inst0_z_0_x(.in(wire_z_0_x_a_y_out), .out(wire_a_y_Foo_inst0_z_0_x_out));
coreir_wire #(.width(1)) wire_z_0_x_Foo_inst0_z_1_x(.in(z_0_x), .out(wire_z_0_x_Foo_inst0_z_1_x_out));
coreir_wire #(.width(1)) wire_z_0_x_a_y(.in(z_0_x), .out(wire_z_0_x_a_y_out));
assign z_0_y = wire_a_x_z_0_y_out[0];
assign z_1_y = wire_Foo_inst0_z_1_y_z_1_y_out[0];
endmodule

