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
wire coreir_lut14_inst0_out;
wire coreir_lut15_inst0_out;
wire coreir_lut15_inst1_out;
wire coreir_lut15_inst2_out;
wire coreir_lut5_inst0_out;
wire coreir_lut9_inst0_out;
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
    .init(4'he),
    .N(2)
) coreir_lut14_inst0 (
    .in(I),
    .out(coreir_lut14_inst0_out)
);
lutN #(
    .init(4'hf),
    .N(2)
) coreir_lut15_inst0 (
    .in(I),
    .out(coreir_lut15_inst0_out)
);
lutN #(
    .init(4'hf),
    .N(2)
) coreir_lut15_inst1 (
    .in(I),
    .out(coreir_lut15_inst1_out)
);
lutN #(
    .init(4'hf),
    .N(2)
) coreir_lut15_inst2 (
    .in(I),
    .out(coreir_lut15_inst2_out)
);
lutN #(
    .init(4'h5),
    .N(2)
) coreir_lut5_inst0 (
    .in(I),
    .out(coreir_lut5_inst0_out)
);
lutN #(
    .init(4'h9),
    .N(2)
) coreir_lut9_inst0 (
    .in(I),
    .out(coreir_lut9_inst0_out)
);
assign O = {coreir_lut15_inst2_out,coreir_lut9_inst0_out,coreir_lut14_inst0_out,coreir_lut5_inst0_out,coreir_lut15_inst1_out,coreir_lut15_inst0_out,coreir_lut13_inst0_out,coreir_lut10_inst0_out};
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

