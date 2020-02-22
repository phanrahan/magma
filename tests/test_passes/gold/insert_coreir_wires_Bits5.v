module coreir_wire #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = in;
endmodule

module Main (
    input [4:0] I,
    output [4:0] O
);
wire [4:0] x_out;
coreir_wire #(
    .width(5)
) x (
    .in(I),
    .out(x_out)
);
assign O = x_out;
endmodule

