module coreir_undriven #(
    parameter width = 1
) (
    output [width-1:0] out
);

endmodule

module corebit_undriven (
    output out
);

endmodule

module Circuit (
    output O0,
    output [4:0] O1,
    output O2_B,
    output O2_C,
    output O3_0_B,
    output O3_0_C,
    output O3_1_B,
    output O3_1_C,
    output O3_2_B,
    output O3_2_C,
    output O3_3_B,
    output O3_3_C,
    output O3_4_B,
    output O3_4_C
);
wire corebit_undriven_inst0_out;
wire corebit_undriven_inst1_out;
wire corebit_undriven_inst10_out;
wire corebit_undriven_inst11_out;
wire corebit_undriven_inst12_out;
wire corebit_undriven_inst2_out;
wire corebit_undriven_inst3_out;
wire corebit_undriven_inst4_out;
wire corebit_undriven_inst5_out;
wire corebit_undriven_inst6_out;
wire corebit_undriven_inst7_out;
wire corebit_undriven_inst8_out;
wire corebit_undriven_inst9_out;
wire [4:0] undriven_inst0_out;
corebit_undriven corebit_undriven_inst0 (
    .out(corebit_undriven_inst0_out)
);
corebit_undriven corebit_undriven_inst1 (
    .out(corebit_undriven_inst1_out)
);
corebit_undriven corebit_undriven_inst10 (
    .out(corebit_undriven_inst10_out)
);
corebit_undriven corebit_undriven_inst11 (
    .out(corebit_undriven_inst11_out)
);
corebit_undriven corebit_undriven_inst12 (
    .out(corebit_undriven_inst12_out)
);
corebit_undriven corebit_undriven_inst2 (
    .out(corebit_undriven_inst2_out)
);
corebit_undriven corebit_undriven_inst3 (
    .out(corebit_undriven_inst3_out)
);
corebit_undriven corebit_undriven_inst4 (
    .out(corebit_undriven_inst4_out)
);
corebit_undriven corebit_undriven_inst5 (
    .out(corebit_undriven_inst5_out)
);
corebit_undriven corebit_undriven_inst6 (
    .out(corebit_undriven_inst6_out)
);
corebit_undriven corebit_undriven_inst7 (
    .out(corebit_undriven_inst7_out)
);
corebit_undriven corebit_undriven_inst8 (
    .out(corebit_undriven_inst8_out)
);
corebit_undriven corebit_undriven_inst9 (
    .out(corebit_undriven_inst9_out)
);
coreir_undriven #(
    .width(5)
) undriven_inst0 (
    .out(undriven_inst0_out)
);
assign O0 = corebit_undriven_inst0_out;
assign O1 = undriven_inst0_out;
assign O2_B = corebit_undriven_inst1_out;
assign O2_C = corebit_undriven_inst2_out;
assign O3_0_B = corebit_undriven_inst3_out;
assign O3_0_C = corebit_undriven_inst4_out;
assign O3_1_B = corebit_undriven_inst5_out;
assign O3_1_C = corebit_undriven_inst6_out;
assign O3_2_B = corebit_undriven_inst7_out;
assign O3_2_C = corebit_undriven_inst8_out;
assign O3_3_B = corebit_undriven_inst9_out;
assign O3_3_C = corebit_undriven_inst10_out;
assign O3_4_B = corebit_undriven_inst11_out;
assign O3_4_C = corebit_undriven_inst12_out;
endmodule

