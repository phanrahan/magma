module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module WrappedWire (input [4:0] I, output [4:0] O);
wire [4:0] wire_x_O_out;
coreir_wire #(.width(5)) wire_x_O(.in(I), .out(wire_x_O_out));
assign O = wire_x_O_out;
endmodule

module Main (input [4:0] I, output [4:0] O);
wire [4:0] wire_x_O_O;
WrappedWire wire_x_O(.I(I), .O(wire_x_O_O));
assign O = wire_x_O_O;
endmodule

