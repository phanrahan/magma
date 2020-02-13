// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input I, output O);
wire Foo_inst0_O;
wire [0:0] x_out;
Foo Foo_inst0(.I(I), .O(Foo_inst0_O));
coreir_wire #(.width(1)) x(.in(Foo_inst0_O), .out(x_out));
assign O = x_out[0];
endmodule

