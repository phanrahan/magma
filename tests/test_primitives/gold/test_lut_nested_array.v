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
wire [0:0] coreir_lut0_inst0_in;
wire coreir_lut0_inst0_out;
wire [0:0] coreir_lut2_inst0_in;
wire coreir_lut2_inst0_out;
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
assign coreir_lut3_inst1_in = I;
lutN #(
    .init(2'h3),
    .N(1)
) coreir_lut3_inst1 (
    .in(coreir_lut3_inst1_in),
    .out(coreir_lut3_inst1_out)
);
assign O = '{{coreir_lut2_inst0_out,coreir_lut3_inst1_out},{coreir_lut3_inst0_out,coreir_lut0_inst0_out}};
endmodule

module test_lut_nested_array (
    input [0:0] I,
    output [1:0] O [1:0]
);
wire [0:0] LUT_inst0_I;
wire [1:0] LUT_inst0_O [1:0];
assign LUT_inst0_I = I;
LUT LUT_inst0 (
    .I(LUT_inst0_I),
    .O(LUT_inst0_O)
);
assign O = '{LUT_inst0_O[1],LUT_inst0_O[0]};
endmodule

