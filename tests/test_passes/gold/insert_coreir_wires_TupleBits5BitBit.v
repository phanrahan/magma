module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input [4:0] I__0, input I__1, output [4:0] O__0, output O__1);
wire [5:0] x_out;
coreir_wire #(.width(6)) x(.in({I__1,I__0[4],I__0[3],I__0[2],I__0[1],I__0[0]}), .out(x_out));
assign O__0 = {x_out[4],x_out[3],x_out[2],x_out[1],x_out[0]};
assign O__1 = x_out[5];
endmodule

