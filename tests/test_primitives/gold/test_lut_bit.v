module lutN #(
    parameter N = 1,
    parameter init = 1
) (
    input [N-1:0] in,
    output out
);
  assign out = init[in];
endmodule

module LUT (
    input [1:0] I,
    output O
);
wire coreir_lut5_inst0_out;
lutN #(
    .init(4'h5),
    .N(2)
) coreir_lut5_inst0 (
    .in(I),
    .out(coreir_lut5_inst0_out)
);
assign O = coreir_lut5_inst0_out;
endmodule

module test_lut_bit (
    input [1:0] I,
    output O
);
wire LUT_inst0_O;
LUT LUT_inst0 (
    .I(I),
    .O(LUT_inst0_O)
);
assign O = LUT_inst0_O;
endmodule

