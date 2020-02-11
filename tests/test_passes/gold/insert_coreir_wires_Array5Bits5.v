module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module WrappedWire_unq1 (input [4:0] I_0, input [4:0] I_1, input [4:0] I_2, input [4:0] I_3, input [4:0] I_4, output [4:0] O_0, output [4:0] O_1, output [4:0] O_2, output [4:0] O_3, output [4:0] O_4);
wire [24:0] wire_I_x_out;
coreir_wire #(.width(25)) wire_I_x(.in({I_4[4],I_4[3],I_4[2],I_4[1],I_4[0],I_3[4],I_3[3],I_3[2],I_3[1],I_3[0],I_2[4],I_2[3],I_2[2],I_2[1],I_2[0],I_1[4],I_1[3],I_1[2],I_1[1],I_1[0],I_0[4],I_0[3],I_0[2],I_0[1],I_0[0]}), .out(wire_I_x_out));
assign O_0 = {wire_I_x_out[4],wire_I_x_out[3],wire_I_x_out[2],wire_I_x_out[1],wire_I_x_out[0]};
assign O_1 = {wire_I_x_out[9],wire_I_x_out[8],wire_I_x_out[7],wire_I_x_out[6],wire_I_x_out[5]};
assign O_2 = {wire_I_x_out[14],wire_I_x_out[13],wire_I_x_out[12],wire_I_x_out[11],wire_I_x_out[10]};
assign O_3 = {wire_I_x_out[19],wire_I_x_out[18],wire_I_x_out[17],wire_I_x_out[16],wire_I_x_out[15]};
assign O_4 = {wire_I_x_out[24],wire_I_x_out[23],wire_I_x_out[22],wire_I_x_out[21],wire_I_x_out[20]};
endmodule

module WrappedWire (input [4:0] I_0, input [4:0] I_1, input [4:0] I_2, input [4:0] I_3, input [4:0] I_4, output [4:0] O_0, output [4:0] O_1, output [4:0] O_2, output [4:0] O_3, output [4:0] O_4);
wire [24:0] wire_x_O_out;
coreir_wire #(.width(25)) wire_x_O(.in({I_4[4],I_4[3],I_4[2],I_4[1],I_4[0],I_3[4],I_3[3],I_3[2],I_3[1],I_3[0],I_2[4],I_2[3],I_2[2],I_2[1],I_2[0],I_1[4],I_1[3],I_1[2],I_1[1],I_1[0],I_0[4],I_0[3],I_0[2],I_0[1],I_0[0]}), .out(wire_x_O_out));
assign O_0 = {wire_x_O_out[4],wire_x_O_out[3],wire_x_O_out[2],wire_x_O_out[1],wire_x_O_out[0]};
assign O_1 = {wire_x_O_out[9],wire_x_O_out[8],wire_x_O_out[7],wire_x_O_out[6],wire_x_O_out[5]};
assign O_2 = {wire_x_O_out[14],wire_x_O_out[13],wire_x_O_out[12],wire_x_O_out[11],wire_x_O_out[10]};
assign O_3 = {wire_x_O_out[19],wire_x_O_out[18],wire_x_O_out[17],wire_x_O_out[16],wire_x_O_out[15]};
assign O_4 = {wire_x_O_out[24],wire_x_O_out[23],wire_x_O_out[22],wire_x_O_out[21],wire_x_O_out[20]};
endmodule

module Main (input [4:0] I_0, input [4:0] I_1, input [4:0] I_2, input [4:0] I_3, input [4:0] I_4, output [4:0] O_0, output [4:0] O_1, output [4:0] O_2, output [4:0] O_3, output [4:0] O_4);
wire [4:0] wire_I_x_O_0;
wire [4:0] wire_I_x_O_1;
wire [4:0] wire_I_x_O_2;
wire [4:0] wire_I_x_O_3;
wire [4:0] wire_I_x_O_4;
wire [4:0] wire_x_O_O_0;
wire [4:0] wire_x_O_O_1;
wire [4:0] wire_x_O_O_2;
wire [4:0] wire_x_O_O_3;
wire [4:0] wire_x_O_O_4;
WrappedWire_unq1 wire_I_x(.I_0(I_0), .I_1(I_1), .I_2(I_2), .I_3(I_3), .I_4(I_4), .O_0(wire_I_x_O_0), .O_1(wire_I_x_O_1), .O_2(wire_I_x_O_2), .O_3(wire_I_x_O_3), .O_4(wire_I_x_O_4));
WrappedWire wire_x_O(.I_0(wire_I_x_O_0), .I_1(wire_I_x_O_1), .I_2(wire_I_x_O_2), .I_3(wire_I_x_O_3), .I_4(wire_I_x_O_4), .O_0(wire_x_O_O_0), .O_1(wire_x_O_O_1), .O_2(wire_x_O_O_2), .O_3(wire_x_O_O_3), .O_4(wire_x_O_O_4));
assign O_0 = wire_x_O_O_0;
assign O_1 = wire_x_O_O_1;
assign O_2 = wire_x_O_O_2;
assign O_3 = wire_x_O_O_3;
assign O_4 = wire_x_O_O_4;
endmodule

