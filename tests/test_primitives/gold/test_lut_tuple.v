module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

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
wire coreir_lut1_inst0_out;
wire coreir_lut2_inst0_out;
wire coreir_lut3_inst0_out;
lutN #(
    .init(2'h1),
    .N(1)
) coreir_lut1_inst0 (
    .in(I),
    .out(coreir_lut1_inst0_out)
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
assign O__0 = coreir_lut1_inst0_out;
assign O__1 = {coreir_lut3_inst0_out,coreir_lut2_inst0_out};
endmodule

module test_lut_tuple (
    input [0:0] I,
    output O__0,
    output [1:0] O__1
);
wire [1:0] Const_inst0_out;
wire [1:0] Const_inst1_out;
wire LUT_inst0_O__0;
wire [1:0] LUT_inst0_O__1;
coreir_const #(
    .value(2'h2),
    .width(2)
) Const_inst0 (
    .out(Const_inst0_out)
);
coreir_const #(
    .value(2'h3),
    .width(2)
) Const_inst1 (
    .out(Const_inst1_out)
);
LUT LUT_inst0 (
    .I(I),
    .O__0(LUT_inst0_O__0),
    .O__1(LUT_inst0_O__1)
);
coreir_term #(
    .width(2)
) term_inst0 (
    .in(Const_inst0_out)
);
coreir_term #(
    .width(2)
) term_inst1 (
    .in(Const_inst1_out)
);
assign O__0 = LUT_inst0_O__0;
assign O__1 = LUT_inst0_O__1;
endmodule

