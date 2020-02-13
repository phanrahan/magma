module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input I, output O);
wire [0:0] wire_I_x_out;
wire [0:0] wire_x_O_out;
coreir_wire #(.width(1)) wire_I_x(.in(I), .out(wire_I_x_out));
coreir_wire #(.width(1)) wire_x_O(.in(wire_I_x_out), .out(wire_x_O_out));
assign O = wire_x_O_out[0];
endmodule

