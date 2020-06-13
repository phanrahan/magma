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
    output [7:0] O
);
wire coreir_lut10_inst0_out;
wire coreir_lut13_inst0_out;
wire coreir_lut13_inst1_out;
wire coreir_lut13_inst2_out;
wire coreir_lut13_inst3_out;
wire coreir_lut13_inst4_out;
wire coreir_lut13_inst5_out;
wire coreir_lut13_inst6_out;
lutN #(
    .init(4'ha),
    .N(2)
) coreir_lut10_inst0 (
    .in(I),
    .out(coreir_lut10_inst0_out)
);
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst0 (
    .in(I),
    .out(coreir_lut13_inst0_out)
);
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst1 (
    .in(I),
    .out(coreir_lut13_inst1_out)
);
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst2 (
    .in(I),
    .out(coreir_lut13_inst2_out)
);
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst3 (
    .in(I),
    .out(coreir_lut13_inst3_out)
);
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst4 (
    .in(I),
    .out(coreir_lut13_inst4_out)
);
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst5 (
    .in(I),
    .out(coreir_lut13_inst5_out)
);
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst6 (
    .in(I),
    .out(coreir_lut13_inst6_out)
);
assign O = {coreir_lut13_inst6_out,coreir_lut13_inst5_out,coreir_lut13_inst4_out,coreir_lut13_inst3_out,coreir_lut13_inst2_out,coreir_lut13_inst1_out,coreir_lut13_inst0_out,coreir_lut10_inst0_out};
endmodule

module test_basic_lut (
    input [1:0] I,
    output [7:0] O
);
wire [7:0] LUT_inst0_O;
LUT LUT_inst0 (
    .I(I),
    .O(LUT_inst0_O)
);
assign O = LUT_inst0_O;
endmodule

