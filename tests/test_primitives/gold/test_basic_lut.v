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
wire [1:0] coreir_lut14_inst0_in;
wire coreir_lut14_inst0_out;
wire [1:0] coreir_lut15_inst0_in;
wire coreir_lut15_inst0_out;
wire [1:0] coreir_lut15_inst1_in;
wire coreir_lut15_inst1_out;
wire [1:0] coreir_lut15_inst2_in;
wire coreir_lut15_inst2_out;
wire [1:0] coreir_lut5_inst0_in;
wire coreir_lut5_inst0_out;
wire [1:0] coreir_lut9_inst0_in;
wire coreir_lut9_inst0_out;
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
assign coreir_lut14_inst0_in = I;
lutN #(
    .init(4'he),
    .N(2)
) coreir_lut14_inst0 (
    .in(coreir_lut14_inst0_in),
    .out(coreir_lut14_inst0_out)
);
assign coreir_lut15_inst0_in = I;
lutN #(
    .init(4'hf),
    .N(2)
) coreir_lut15_inst0 (
    .in(coreir_lut15_inst0_in),
    .out(coreir_lut15_inst0_out)
);
assign coreir_lut15_inst1_in = I;
lutN #(
    .init(4'hf),
    .N(2)
) coreir_lut15_inst1 (
    .in(coreir_lut15_inst1_in),
    .out(coreir_lut15_inst1_out)
);
assign coreir_lut15_inst2_in = I;
lutN #(
    .init(4'hf),
    .N(2)
) coreir_lut15_inst2 (
    .in(coreir_lut15_inst2_in),
    .out(coreir_lut15_inst2_out)
);
assign coreir_lut5_inst0_in = I;
lutN #(
    .init(4'h5),
    .N(2)
) coreir_lut5_inst0 (
    .in(coreir_lut5_inst0_in),
    .out(coreir_lut5_inst0_out)
);
assign coreir_lut9_inst0_in = I;
lutN #(
    .init(4'h9),
    .N(2)
) coreir_lut9_inst0 (
    .in(coreir_lut9_inst0_in),
    .out(coreir_lut9_inst0_out)
);
assign O = {coreir_lut15_inst2_out,coreir_lut9_inst0_out,coreir_lut14_inst0_out,coreir_lut5_inst0_out,coreir_lut15_inst1_out,coreir_lut15_inst0_out,coreir_lut13_inst0_out,coreir_lut10_inst0_out};
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

