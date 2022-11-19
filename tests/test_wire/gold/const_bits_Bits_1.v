// Module `Buf` defined externally
module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module main (
    output [0:0] O
);
wire [0:0] buf_O;
wire [0:0] const_1_1_out;
Buf buf (
    .I(const_1_1_out),
    .O(buf_O)
);
coreir_const #(
    .value(1'h1),
    .width(1)
) const_1_1 (
    .out(const_1_1_out)
);
assign O = \buf _O;
endmodule

