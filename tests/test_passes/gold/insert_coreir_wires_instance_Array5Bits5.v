// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input [4:0] I_0, input [4:0] I_1, input [4:0] I_2, input [4:0] I_3, input [4:0] I_4, output [4:0] O_0, output [4:0] O_1, output [4:0] O_2, output [4:0] O_3, output [4:0] O_4);
wire [4:0] Foo_inst0_O_0;
wire [4:0] Foo_inst0_O_1;
wire [4:0] Foo_inst0_O_2;
wire [4:0] Foo_inst0_O_3;
wire [4:0] Foo_inst0_O_4;
wire [24:0] wire_x_O_out;
Foo Foo_inst0(.I_0(I_0), .I_1(I_1), .I_2(I_2), .I_3(I_3), .I_4(I_4), .O_0(Foo_inst0_O_0), .O_1(Foo_inst0_O_1), .O_2(Foo_inst0_O_2), .O_3(Foo_inst0_O_3), .O_4(Foo_inst0_O_4));
coreir_wire #(.width(25)) wire_x_O(.in({Foo_inst0_O_4[4],Foo_inst0_O_4[3],Foo_inst0_O_4[2],Foo_inst0_O_4[1],Foo_inst0_O_4[0],Foo_inst0_O_3[4],Foo_inst0_O_3[3],Foo_inst0_O_3[2],Foo_inst0_O_3[1],Foo_inst0_O_3[0],Foo_inst0_O_2[4],Foo_inst0_O_2[3],Foo_inst0_O_2[2],Foo_inst0_O_2[1],Foo_inst0_O_2[0],Foo_inst0_O_1[4],Foo_inst0_O_1[3],Foo_inst0_O_1[2],Foo_inst0_O_1[1],Foo_inst0_O_1[0],Foo_inst0_O_0[4],Foo_inst0_O_0[3],Foo_inst0_O_0[2],Foo_inst0_O_0[1],Foo_inst0_O_0[0]}), .out(wire_x_O_out));
assign O_0 = {wire_x_O_out[4],wire_x_O_out[3],wire_x_O_out[2],wire_x_O_out[1],wire_x_O_out[0]};
assign O_1 = {wire_x_O_out[9],wire_x_O_out[8],wire_x_O_out[7],wire_x_O_out[6],wire_x_O_out[5]};
assign O_2 = {wire_x_O_out[14],wire_x_O_out[13],wire_x_O_out[12],wire_x_O_out[11],wire_x_O_out[10]};
assign O_3 = {wire_x_O_out[19],wire_x_O_out[18],wire_x_O_out[17],wire_x_O_out[16],wire_x_O_out[15]};
assign O_4 = {wire_x_O_out[24],wire_x_O_out[23],wire_x_O_out[22],wire_x_O_out[21],wire_x_O_out[20]};
endmodule

