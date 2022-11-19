// Module `Buf` defined externally
module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module main (
    output O
);
wire bit_const_1_None_out;
wire buf_O;
corebit_const #(
    .value(1'b1)
) bit_const_1_None (
    .out(bit_const_1_None_out)
);
Buf buf (
    .I(bit_const_1_None_out),
    .O(buf_O)
);
assign O = \buf _O;
endmodule

