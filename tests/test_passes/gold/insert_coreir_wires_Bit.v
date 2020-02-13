module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input I, output O);
wire [0:0] x_out;
coreir_wire #(.width(1)) x(.in(I), .out(x_out));
assign O = x_out[0];
endmodule

