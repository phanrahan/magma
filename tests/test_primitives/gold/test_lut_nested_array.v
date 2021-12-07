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
    input [0:0] I,
    output [1:0] O [1:0]
);
wire coreir_lut1_inst0_out;
wire coreir_lut1_inst1_out;
wire coreir_lut1_inst2_out;
wire coreir_lut2_inst0_out;
lutN #(
    .init(2'h1),
    .N(1)
) coreir_lut1_inst0 (
    .in(I),
    .out(coreir_lut1_inst0_out)
);
lutN #(
    .init(2'h1),
    .N(1)
) coreir_lut1_inst1 (
    .in(I),
    .out(coreir_lut1_inst1_out)
);
lutN #(
    .init(2'h1),
    .N(1)
) coreir_lut1_inst2 (
    .in(I),
    .out(coreir_lut1_inst2_out)
);
lutN #(
    .init(2'h2),
    .N(1)
) coreir_lut2_inst0 (
    .in(I),
    .out(coreir_lut2_inst0_out)
);
assign O[1] = {coreir_lut2_inst0_out,coreir_lut1_inst2_out};
assign O[0] = {coreir_lut1_inst1_out,coreir_lut1_inst0_out};
endmodule

module test_lut_nested_array (
    input [0:0] I,
    output [1:0] O [1:0]
);
wire [1:0] LUT_inst0_O [1:0];
LUT LUT_inst0 (
    .I(I),
    .O(LUT_inst0_O)
);
assign O[1] = LUT_inst0_O[1];
assign O[0] = LUT_inst0_O[0];
endmodule

