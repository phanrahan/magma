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
    output O_0_X,
    output [1:0] O_0_Y,
    output O_1_X,
    output [1:0] O_1_Y
);
wire [0:0] coreir_lut0_inst0_in;
wire coreir_lut0_inst0_out;
wire [0:0] coreir_lut1_inst0_in;
wire coreir_lut1_inst0_out;
wire [0:0] coreir_lut2_inst0_in;
wire coreir_lut2_inst0_out;
wire [0:0] coreir_lut2_inst1_in;
wire coreir_lut2_inst1_out;
wire [0:0] coreir_lut3_inst0_in;
wire coreir_lut3_inst0_out;
wire [0:0] coreir_lut3_inst1_in;
wire coreir_lut3_inst1_out;
assign coreir_lut0_inst0_in = I;
lutN #(
    .init(2'h0),
    .N(1)
) coreir_lut0_inst0 (
    .in(coreir_lut0_inst0_in),
    .out(coreir_lut0_inst0_out)
);
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
assign coreir_lut2_inst1_in = I;
lutN #(
    .init(2'h2),
    .N(1)
) coreir_lut2_inst1 (
    .in(coreir_lut2_inst1_in),
    .out(coreir_lut2_inst1_out)
);
assign coreir_lut3_inst0_in = I;
lutN #(
    .init(2'h3),
    .N(1)
) coreir_lut3_inst0 (
    .in(coreir_lut3_inst0_in),
    .out(coreir_lut3_inst0_out)
);
assign coreir_lut3_inst1_in = I;
lutN #(
    .init(2'h3),
    .N(1)
) coreir_lut3_inst1 (
    .in(coreir_lut3_inst1_in),
    .out(coreir_lut3_inst1_out)
);
assign O_0_X = coreir_lut1_inst0_out;
assign O_0_Y = {coreir_lut3_inst0_out,coreir_lut0_inst0_out};
assign O_1_X = coreir_lut2_inst0_out;
assign O_1_Y = {coreir_lut2_inst1_out,coreir_lut3_inst1_out};
endmodule

module test_lut_arr_of_product (
    input [0:0] I,
    output O_0_X,
    output [1:0] O_0_Y,
    output O_1_X,
    output [1:0] O_1_Y
);
wire [0:0] LUT_inst0_I;
wire LUT_inst0_O_0_X;
wire [1:0] LUT_inst0_O_0_Y;
wire LUT_inst0_O_1_X;
wire [1:0] LUT_inst0_O_1_Y;
assign LUT_inst0_I = I;
LUT LUT_inst0 (
    .I(LUT_inst0_I),
    .O_0_X(LUT_inst0_O_0_X),
    .O_0_Y(LUT_inst0_O_0_Y),
    .O_1_X(LUT_inst0_O_1_X),
    .O_1_Y(LUT_inst0_O_1_Y)
);
assign O_0_X = LUT_inst0_O_0_X;
assign O_0_Y = LUT_inst0_O_0_Y;
assign O_1_X = LUT_inst0_O_1_X;
assign O_1_Y = LUT_inst0_O_1_Y;
endmodule

