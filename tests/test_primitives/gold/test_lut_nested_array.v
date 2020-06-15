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
    output [1:0] O_0,
    output [1:0] O_1
);
wire coreir_lut0_inst0_out;
wire coreir_lut2_inst0_out;
wire coreir_lut3_inst0_out;
wire coreir_lut3_inst1_out;
lutN #(
    .init(2'h0),
    .N(1)
) coreir_lut0_inst0 (
    .in(I),
    .out(coreir_lut0_inst0_out)
);
lutN #(
    .init(2'h2),
    .N(1)
) coreir_lut2_inst0 (
    .in(I),
    .out(coreir_lut2_inst0_out)
);
lutN #(
    .init(2'h3),
    .N(1)
) coreir_lut3_inst0 (
    .in(I),
    .out(coreir_lut3_inst0_out)
);
lutN #(
    .init(2'h3),
    .N(1)
) coreir_lut3_inst1 (
    .in(I),
    .out(coreir_lut3_inst1_out)
);
assign O_0 = {coreir_lut3_inst0_out,coreir_lut0_inst0_out};
assign O_1 = {coreir_lut2_inst0_out,coreir_lut3_inst1_out};
endmodule

module test_lut_nested_array (
    input [0:0] I,
    output [1:0] O_0,
    output [1:0] O_1
);
wire [1:0] LUT_inst0_O_0;
wire [1:0] LUT_inst0_O_1;
LUT LUT_inst0 (
    .I(I),
    .O_0(LUT_inst0_O_0),
    .O_1(LUT_inst0_O_1)
);
assign O_0 = LUT_inst0_O_0;
assign O_1 = LUT_inst0_O_1;
endmodule

