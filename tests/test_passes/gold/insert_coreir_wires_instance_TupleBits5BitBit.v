// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module WrappedWire_unq2 (input [4:0] I__0, input I__1, output [4:0] O__0, output O__1);
wire [5:0] wire_Foo_inst0_O_x_out;
coreir_wire #(.width(6)) wire_Foo_inst0_O_x(.in({I__1,I__0[4],I__0[3],I__0[2],I__0[1],I__0[0]}), .out(wire_Foo_inst0_O_x_out));
assign O__0 = {wire_Foo_inst0_O_x_out[4],wire_Foo_inst0_O_x_out[3],wire_Foo_inst0_O_x_out[2],wire_Foo_inst0_O_x_out[1],wire_Foo_inst0_O_x_out[0]};
assign O__1 = wire_Foo_inst0_O_x_out[5];
endmodule

module WrappedWire_unq1 (input [4:0] I__0, input I__1, output [4:0] O__0, output O__1);
wire [5:0] wire_x_O_out;
coreir_wire #(.width(6)) wire_x_O(.in({I__1,I__0[4],I__0[3],I__0[2],I__0[1],I__0[0]}), .out(wire_x_O_out));
assign O__0 = {wire_x_O_out[4],wire_x_O_out[3],wire_x_O_out[2],wire_x_O_out[1],wire_x_O_out[0]};
assign O__1 = wire_x_O_out[5];
endmodule

module WrappedWire (input [4:0] I__0, input I__1, output [4:0] O__0, output O__1);
wire [5:0] wire_I_Foo_inst0_I_out;
coreir_wire #(.width(6)) wire_I_Foo_inst0_I(.in({I__1,I__0[4],I__0[3],I__0[2],I__0[1],I__0[0]}), .out(wire_I_Foo_inst0_I_out));
assign O__0 = {wire_I_Foo_inst0_I_out[4],wire_I_Foo_inst0_I_out[3],wire_I_Foo_inst0_I_out[2],wire_I_Foo_inst0_I_out[1],wire_I_Foo_inst0_I_out[0]};
assign O__1 = wire_I_Foo_inst0_I_out[5];
endmodule

module Main (input [4:0] I__0, input I__1, output [4:0] O__0, output O__1);
wire [4:0] Foo_inst0_O__0;
wire Foo_inst0_O__1;
wire [4:0] wire_Foo_inst0_O_x_O__0;
wire wire_Foo_inst0_O_x_O__1;
wire [4:0] wire_I_Foo_inst0_I_O__0;
wire wire_I_Foo_inst0_I_O__1;
wire [4:0] wire_x_O_O__0;
wire wire_x_O_O__1;
Foo Foo_inst0(.I__0(wire_I_Foo_inst0_I_O__0), .I__1(wire_I_Foo_inst0_I_O__1), .O__0(Foo_inst0_O__0), .O__1(Foo_inst0_O__1));
WrappedWire_unq2 wire_Foo_inst0_O_x(.I__0(Foo_inst0_O__0), .I__1(Foo_inst0_O__1), .O__0(wire_Foo_inst0_O_x_O__0), .O__1(wire_Foo_inst0_O_x_O__1));
WrappedWire wire_I_Foo_inst0_I(.I__0(I__0), .I__1(I__1), .O__0(wire_I_Foo_inst0_I_O__0), .O__1(wire_I_Foo_inst0_I_O__1));
WrappedWire_unq1 wire_x_O(.I__0(wire_Foo_inst0_O_x_O__0), .I__1(wire_Foo_inst0_O_x_O__1), .O__0(wire_x_O_O__0), .O__1(wire_x_O_O__1));
assign O__0 = wire_x_O_O__0;
assign O__1 = wire_x_O_O__1;
endmodule

