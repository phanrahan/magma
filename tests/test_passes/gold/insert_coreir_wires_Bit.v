module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module WrappedWire_unq1 (input I, output O);
wire [0:0] wire_I_x_out;
coreir_wire #(.width(1)) wire_I_x(.in(I), .out(wire_I_x_out));
assign O = wire_I_x_out[0];
endmodule

module WrappedWire (input I, output O);
wire [0:0] wire_x_O_out;
coreir_wire #(.width(1)) wire_x_O(.in(I), .out(wire_x_O_out));
assign O = wire_x_O_out[0];
endmodule

module Main (input I, output O);
wire wire_I_x_O;
wire wire_x_O_O;
WrappedWire_unq1 wire_I_x(.I(I), .O(wire_I_x_O));
WrappedWire wire_x_O(.I(wire_I_x_O), .O(wire_x_O_O));
assign O = wire_x_O_O;
endmodule

