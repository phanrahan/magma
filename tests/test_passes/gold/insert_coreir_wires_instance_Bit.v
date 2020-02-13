// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input I, output O);
wire Foo_inst0_O;
wire [0:0] wire_Foo_inst0_O_x_out;
wire [0:0] wire_I_Foo_inst0_I_out;
wire [0:0] wire_x_O_out;
Foo Foo_inst0(.I(wire_I_Foo_inst0_I_out[0]), .O(Foo_inst0_O));
coreir_wire #(.width(1)) wire_Foo_inst0_O_x(.in(Foo_inst0_O), .out(wire_Foo_inst0_O_x_out));
coreir_wire #(.width(1)) wire_I_Foo_inst0_I(.in(I), .out(wire_I_Foo_inst0_I_out));
coreir_wire #(.width(1)) wire_x_O(.in(wire_Foo_inst0_O_x_out), .out(wire_x_O_out));
assign O = wire_x_O_out[0];
endmodule

