module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input [4:0] I, output [4:0] O);
wire [4:0] wire_I_x_out;
wire [4:0] wire_x_O_out;
coreir_wire #(.width(5)) wire_I_x(.in(I), .out(wire_I_x_out));
coreir_wire #(.width(5)) wire_x_O(.in(wire_I_x_out), .out(wire_x_O_out));
assign O = wire_x_O_out;
endmodule

