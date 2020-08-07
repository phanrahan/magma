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
wire [1:0] coreir_lut10_inst0_in;
wire coreir_lut10_inst0_out;
wire [1:0] coreir_lut13_inst0_in;
wire coreir_lut13_inst0_out;
wire [1:0] coreir_lut13_inst1_in;
wire coreir_lut13_inst1_out;
wire [1:0] coreir_lut13_inst2_in;
wire coreir_lut13_inst2_out;
wire [1:0] coreir_lut13_inst3_in;
wire coreir_lut13_inst3_out;
wire [1:0] coreir_lut13_inst4_in;
wire coreir_lut13_inst4_out;
wire [1:0] coreir_lut13_inst5_in;
wire coreir_lut13_inst5_out;
wire [1:0] coreir_lut13_inst6_in;
wire coreir_lut13_inst6_out;
assign coreir_lut10_inst0_in = I;
lutN #(
    .init(4'ha),
    .N(2)
) coreir_lut10_inst0 (
    .in(coreir_lut10_inst0_in),
    .out(coreir_lut10_inst0_out)
);
assign coreir_lut13_inst0_in = I;
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst0 (
    .in(coreir_lut13_inst0_in),
    .out(coreir_lut13_inst0_out)
);
assign coreir_lut13_inst1_in = I;
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst1 (
    .in(coreir_lut13_inst1_in),
    .out(coreir_lut13_inst1_out)
);
assign coreir_lut13_inst2_in = I;
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst2 (
    .in(coreir_lut13_inst2_in),
    .out(coreir_lut13_inst2_out)
);
assign coreir_lut13_inst3_in = I;
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst3 (
    .in(coreir_lut13_inst3_in),
    .out(coreir_lut13_inst3_out)
);
assign coreir_lut13_inst4_in = I;
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst4 (
    .in(coreir_lut13_inst4_in),
    .out(coreir_lut13_inst4_out)
);
assign coreir_lut13_inst5_in = I;
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst5 (
    .in(coreir_lut13_inst5_in),
    .out(coreir_lut13_inst5_out)
);
assign coreir_lut13_inst6_in = I;
lutN #(
    .init(4'hd),
    .N(2)
) coreir_lut13_inst6 (
    .in(coreir_lut13_inst6_in),
    .out(coreir_lut13_inst6_out)
);
assign O = {coreir_lut13_inst6_out,coreir_lut13_inst5_out,coreir_lut13_inst4_out,coreir_lut13_inst3_out,coreir_lut13_inst2_out,coreir_lut13_inst1_out,coreir_lut13_inst0_out,coreir_lut10_inst0_out};
endmodule

module test_basic_lut (
    input [1:0] I,
    output [7:0] O
);
wire [1:0] LUT_inst0_I;
wire [7:0] LUT_inst0_O;
assign LUT_inst0_I = I;
LUT LUT_inst0 (
    .I(LUT_inst0_I),
    .O(LUT_inst0_O)
);
assign O = LUT_inst0_O;
endmodule

