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
wire [1:0] coreir_lut5_inst0_in;
wire coreir_lut5_inst0_out;
assign coreir_lut5_inst0_in = I;
lutN #(
    .init(4'h5),
    .N(2)
) coreir_lut5_inst0 (
    .in(coreir_lut5_inst0_in),
    .out(coreir_lut5_inst0_out)
);
assign O = coreir_lut5_inst0_out;
endmodule

module test_lut_bit (
    input [1:0] I,
    output O
);
wire [1:0] LUT_inst0_I;
wire LUT_inst0_O;
assign LUT_inst0_I = I;
LUT LUT_inst0 (
    .I(LUT_inst0_I),
    .O(LUT_inst0_O)
);
assign O = LUT_inst0_O;
endmodule

