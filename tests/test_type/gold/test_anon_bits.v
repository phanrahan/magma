module coreir_wire #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = in;
endmodule

module Test (
    input [4:0] I,
    output [4:0] O
);
wire [4:0] x_out;
wire [4:0] y_out;
coreir_wire #(
    .width(5)
) x (
    .in(y_out),
    .out(x_out)
);
coreir_wire #(
    .width(5)
) y (
    .in(I),
    .out(y_out)
);
assign O = x_out;
endmodule

