// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input z_x, output z_y);
wire Foo_inst0_z_y;
wire [0:0] a_x_out;
wire [0:0] a_y_out;
Foo Foo_inst0(.z_x(a_y_out[0]), .z_y(Foo_inst0_z_y));
coreir_wire #(.width(1)) a_x(.in(Foo_inst0_z_y), .out(a_x_out));
coreir_wire #(.width(1)) a_y(.in(z_x), .out(a_y_out));
assign z_y = a_x_out[0];
endmodule

