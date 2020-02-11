// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module WrappedWire_unq5 (input I, output O);
wire [0:0] wire_Foo_inst0_z_1_y_z_1_y_out;
coreir_wire #(.width(1)) wire_Foo_inst0_z_1_y_z_1_y(.in(I), .out(wire_Foo_inst0_z_1_y_z_1_y_out));
assign O = wire_Foo_inst0_z_1_y_z_1_y_out[0];
endmodule

module WrappedWire_unq4 (input I, output O);
wire [0:0] wire_Foo_inst0_z_0_y_a_x_out;
coreir_wire #(.width(1)) wire_Foo_inst0_z_0_y_a_x(.in(I), .out(wire_Foo_inst0_z_0_y_a_x_out));
assign O = wire_Foo_inst0_z_0_y_a_x_out[0];
endmodule

module WrappedWire_unq3 (input I, output O);
wire [0:0] wire_a_x_z_0_y_out;
coreir_wire #(.width(1)) wire_a_x_z_0_y(.in(I), .out(wire_a_x_z_0_y_out));
assign O = wire_a_x_z_0_y_out[0];
endmodule

module WrappedWire_unq2 (input I, output O);
wire [0:0] wire_z_0_x_Foo_inst0_z_1_x_out;
coreir_wire #(.width(1)) wire_z_0_x_Foo_inst0_z_1_x(.in(I), .out(wire_z_0_x_Foo_inst0_z_1_x_out));
assign O = wire_z_0_x_Foo_inst0_z_1_x_out[0];
endmodule

module WrappedWire_unq1 (input I, output O);
wire [0:0] wire_z_0_x_a_y_out;
coreir_wire #(.width(1)) wire_z_0_x_a_y(.in(I), .out(wire_z_0_x_a_y_out));
assign O = wire_z_0_x_a_y_out[0];
endmodule

module WrappedWire (input I, output O);
wire [0:0] wire_a_y_Foo_inst0_z_0_x_out;
coreir_wire #(.width(1)) wire_a_y_Foo_inst0_z_0_x(.in(I), .out(wire_a_y_Foo_inst0_z_0_x_out));
assign O = wire_a_y_Foo_inst0_z_0_x_out[0];
endmodule

module Main (input z_0_x, output z_0_y, input z_1_x, output z_1_y);
wire Foo_inst0_z_0_y;
wire Foo_inst0_z_1_y;
wire wire_Foo_inst0_z_0_y_a_x_O;
wire wire_Foo_inst0_z_1_y_z_1_y_O;
wire wire_a_x_z_0_y_O;
wire wire_a_y_Foo_inst0_z_0_x_O;
wire wire_z_0_x_Foo_inst0_z_1_x_O;
wire wire_z_0_x_a_y_O;
Foo Foo_inst0(.z_0_x(wire_a_y_Foo_inst0_z_0_x_O), .z_0_y(Foo_inst0_z_0_y), .z_1_x(wire_z_0_x_Foo_inst0_z_1_x_O), .z_1_y(Foo_inst0_z_1_y));
WrappedWire_unq4 wire_Foo_inst0_z_0_y_a_x(.I(Foo_inst0_z_0_y), .O(wire_Foo_inst0_z_0_y_a_x_O));
WrappedWire_unq5 wire_Foo_inst0_z_1_y_z_1_y(.I(Foo_inst0_z_1_y), .O(wire_Foo_inst0_z_1_y_z_1_y_O));
WrappedWire_unq3 wire_a_x_z_0_y(.I(wire_Foo_inst0_z_0_y_a_x_O), .O(wire_a_x_z_0_y_O));
WrappedWire wire_a_y_Foo_inst0_z_0_x(.I(wire_z_0_x_a_y_O), .O(wire_a_y_Foo_inst0_z_0_x_O));
WrappedWire_unq2 wire_z_0_x_Foo_inst0_z_1_x(.I(z_0_x), .O(wire_z_0_x_Foo_inst0_z_1_x_O));
WrappedWire_unq1 wire_z_0_x_a_y(.I(z_0_x), .O(wire_z_0_x_a_y_O));
assign z_0_y = wire_a_x_z_0_y_O;
assign z_1_y = wire_Foo_inst0_z_1_y_z_1_y_O;
endmodule

