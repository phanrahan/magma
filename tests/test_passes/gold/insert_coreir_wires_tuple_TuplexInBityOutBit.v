// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module WrappedWire_unq3 (input I, output O);
wire [0:0] wire_Foo_inst0_z_y_a_x_out;
coreir_wire #(.width(1)) wire_Foo_inst0_z_y_a_x(.in(I), .out(wire_Foo_inst0_z_y_a_x_out));
assign O = wire_Foo_inst0_z_y_a_x_out[0];
endmodule

module WrappedWire_unq2 (input I, output O);
wire [0:0] wire_a_x_z_y_out;
coreir_wire #(.width(1)) wire_a_x_z_y(.in(I), .out(wire_a_x_z_y_out));
assign O = wire_a_x_z_y_out[0];
endmodule

module WrappedWire_unq1 (input I, output O);
wire [0:0] wire_z_x_a_y_out;
coreir_wire #(.width(1)) wire_z_x_a_y(.in(I), .out(wire_z_x_a_y_out));
assign O = wire_z_x_a_y_out[0];
endmodule

module WrappedWire (input I, output O);
wire [0:0] wire_a_y_Foo_inst0_z_x_out;
coreir_wire #(.width(1)) wire_a_y_Foo_inst0_z_x(.in(I), .out(wire_a_y_Foo_inst0_z_x_out));
assign O = wire_a_y_Foo_inst0_z_x_out[0];
endmodule

module Main (input z_x, output z_y);
wire Foo_inst0_z_y;
wire wire_Foo_inst0_z_y_a_x_O;
wire wire_a_x_z_y_O;
wire wire_a_y_Foo_inst0_z_x_O;
wire wire_z_x_a_y_O;
Foo Foo_inst0(.z_x(wire_a_y_Foo_inst0_z_x_O), .z_y(Foo_inst0_z_y));
WrappedWire_unq3 wire_Foo_inst0_z_y_a_x(.I(Foo_inst0_z_y), .O(wire_Foo_inst0_z_y_a_x_O));
WrappedWire_unq2 wire_a_x_z_y(.I(wire_Foo_inst0_z_y_a_x_O), .O(wire_a_x_z_y_O));
WrappedWire wire_a_y_Foo_inst0_z_x(.I(wire_z_x_a_y_O), .O(wire_a_y_Foo_inst0_z_x_O));
WrappedWire_unq1 wire_z_x_a_y(.I(z_x), .O(wire_z_x_a_y_O));
assign z_y = wire_a_x_z_y_O;
endmodule

