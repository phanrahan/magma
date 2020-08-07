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
    output O__0,
    output [1:0] O__1
);
wire [0:0] coreir_lut1_inst0_in;
wire coreir_lut1_inst0_out;
wire [0:0] coreir_lut2_inst0_in;
wire coreir_lut2_inst0_out;
wire [0:0] coreir_lut3_inst0_in;
wire coreir_lut3_inst0_out;
assign coreir_lut1_inst0_in = I;
lutN #(
    .init(2'h1),
    .N(1)
) coreir_lut1_inst0 (
    .in(coreir_lut1_inst0_in),
    .out(coreir_lut1_inst0_out)
);
assign coreir_lut2_inst0_in = I;
lutN #(
    .init(2'h2),
    .N(1)
) coreir_lut2_inst0 (
    .in(coreir_lut2_inst0_in),
    .out(coreir_lut2_inst0_out)
);
assign coreir_lut3_inst0_in = I;
lutN #(
    .init(2'h3),
    .N(1)
) coreir_lut3_inst0 (
    .in(coreir_lut3_inst0_in),
    .out(coreir_lut3_inst0_out)
);
assign O__0 = coreir_lut1_inst0_out;
assign O__1 = {coreir_lut2_inst0_out,coreir_lut3_inst0_out};
endmodule

module test_lut_tuple (
    input [0:0] I,
    output O__0,
    output [1:0] O__1
);
wire [0:0] LUT_inst0_I;
wire LUT_inst0_O__0;
wire [1:0] LUT_inst0_O__1;
assign LUT_inst0_I = I;
LUT LUT_inst0 (
    .I(LUT_inst0_I),
    .O__0(LUT_inst0_O__0),
    .O__1(LUT_inst0_O__1)
);
assign O__0 = LUT_inst0_O__0;
assign O__1 = LUT_inst0_O__1;
endmodule

