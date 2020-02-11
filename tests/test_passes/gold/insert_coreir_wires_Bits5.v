module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module WrappedWire_unq1 (input [4:0] I, output [4:0] O);
wire [4:0] wire_I_x_out;
coreir_wire #(.width(5)) wire_I_x(.in(I), .out(wire_I_x_out));
assign O = wire_I_x_out;
endmodule

module WrappedWire (input [4:0] I, output [4:0] O);
wire [4:0] wire_x_O_out;
coreir_wire #(.width(5)) wire_x_O(.in(I), .out(wire_x_O_out));
assign O = wire_x_O_out;
endmodule

module Main (input [4:0] I, output [4:0] O);
wire [4:0] wire_I_x_O;
wire [4:0] wire_x_O_O;
WrappedWire_unq1 wire_I_x(.I(I), .O(wire_I_x_O));
WrappedWire wire_x_O(.I(wire_I_x_O), .O(wire_x_O_O));
assign O = wire_x_O_O;
endmodule

