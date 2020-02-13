// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input z_0_x, output z_0_y, input z_1_x, output z_1_y);
wire Foo_inst0_z_0_y;
wire Foo_inst0_z_1_y;
wire [0:0] a_x_out;
wire [0:0] a_y_out;
Foo Foo_inst0(.z_0_x(a_y_out[0]), .z_0_y(Foo_inst0_z_0_y), .z_1_x(z_0_x), .z_1_y(Foo_inst0_z_1_y));
coreir_wire #(.width(1)) a_x(.in(Foo_inst0_z_0_y), .out(a_x_out));
coreir_wire #(.width(1)) a_y(.in(z_0_x), .out(a_y_out));
assign z_0_y = a_x_out[0];
assign z_1_y = Foo_inst0_z_1_y;
endmodule

