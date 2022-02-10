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
    output [2:0] O
);
wire [2:0] Buf_inst0_O;
wire [2:0] const_1_3_out;
Buf Buf_inst0 (
    .I(const_1_3_out),
    .O(Buf_inst0_O)
);
coreir_const #(
    .value(3'h1),
    .width(3)
) const_1_3 (
    .out(const_1_3_out)
);
assign O = Buf_inst0_O;
endmodule

