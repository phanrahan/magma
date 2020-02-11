// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module WrappedWire_unq2 (input I, output O);
wire [0:0] wire_Foo_inst0_O_x_out;
coreir_wire #(.width(1)) wire_Foo_inst0_O_x(.in(I), .out(wire_Foo_inst0_O_x_out));
assign O = wire_Foo_inst0_O_x_out[0];
endmodule

module WrappedWire_unq1 (input I, output O);
wire [0:0] wire_x_O_out;
coreir_wire #(.width(1)) wire_x_O(.in(I), .out(wire_x_O_out));
assign O = wire_x_O_out[0];
endmodule

module WrappedWire (input I, output O);
wire [0:0] wire_I_Foo_inst0_I_out;
coreir_wire #(.width(1)) wire_I_Foo_inst0_I(.in(I), .out(wire_I_Foo_inst0_I_out));
assign O = wire_I_Foo_inst0_I_out[0];
endmodule

module Main (input I, output O);
wire Foo_inst0_O;
wire wire_Foo_inst0_O_x_O;
wire wire_I_Foo_inst0_I_O;
wire wire_x_O_O;
Foo Foo_inst0(.I(wire_I_Foo_inst0_I_O), .O(Foo_inst0_O));
WrappedWire_unq2 wire_Foo_inst0_O_x(.I(Foo_inst0_O), .O(wire_Foo_inst0_O_x_O));
WrappedWire wire_I_Foo_inst0_I(.I(I), .O(wire_I_Foo_inst0_I_O));
WrappedWire_unq1 wire_x_O(.I(wire_Foo_inst0_O_x_O), .O(wire_x_O_O));
assign O = wire_x_O_O;
endmodule

