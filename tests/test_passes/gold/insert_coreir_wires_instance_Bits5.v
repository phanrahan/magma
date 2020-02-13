// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input [4:0] I, output [4:0] O);
wire [4:0] Foo_inst0_O;
wire [4:0] wire_x_O_out;
Foo Foo_inst0(.I(I), .O(Foo_inst0_O));
coreir_wire #(.width(5)) wire_x_O(.in(Foo_inst0_O), .out(wire_x_O_out));
assign O = wire_x_O_out;
endmodule

