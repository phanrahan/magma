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
wire Buf_inst0_O;
wire bit_const_1_None_out;
Buf Buf_inst0 (
    .I(bit_const_1_None_out),
    .O(Buf_inst0_O)
);
corebit_const #(
    .value(1'b1)
) bit_const_1_None (
    .out(bit_const_1_None_out)
);
assign O = Buf_inst0_O;
endmodule

