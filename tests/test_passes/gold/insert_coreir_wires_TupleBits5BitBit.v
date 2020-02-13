module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input [4:0] I__0, input I__1, output [4:0] O__0, output O__1);
wire [5:0] wire_I_x_out;
wire [5:0] wire_x_O_out;
coreir_wire #(.width(6)) wire_I_x(.in({I__1,I__0[4],I__0[3],I__0[2],I__0[1],I__0[0]}), .out(wire_I_x_out));
coreir_wire #(.width(6)) wire_x_O(.in(wire_I_x_out), .out(wire_x_O_out));
assign O__0 = {wire_x_O_out[4],wire_x_O_out[3],wire_x_O_out[2],wire_x_O_out[1],wire_x_O_out[0]};
assign O__1 = wire_x_O_out[5];
endmodule

