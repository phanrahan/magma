module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module corebit_term (
    input in
);

endmodule

module Circuit (
    input I0,
    input [4:0] I1,
    input I2_B,
    input I2_C,
    input I3_0_B,
    input I3_0_C,
    input I3_1_B,
    input I3_1_C,
    input I3_2_B,
    input I3_2_C,
    input I3_3_B,
    input I3_3_C,
    input I3_4_B,
    input I3_4_C
);
wire corebit_term_inst0_in;
wire corebit_term_inst1_in;
wire corebit_term_inst10_in;
wire corebit_term_inst11_in;
wire corebit_term_inst12_in;
wire corebit_term_inst2_in;
wire corebit_term_inst3_in;
wire corebit_term_inst4_in;
wire corebit_term_inst5_in;
wire corebit_term_inst6_in;
wire corebit_term_inst7_in;
wire corebit_term_inst8_in;
wire corebit_term_inst9_in;
wire [4:0] term_inst0_in;
assign corebit_term_inst0_in = I0;
corebit_term corebit_term_inst0 (
    .in(corebit_term_inst0_in)
);
assign corebit_term_inst1_in = I2_B;
corebit_term corebit_term_inst1 (
    .in(corebit_term_inst1_in)
);
assign corebit_term_inst10_in = I3_3_C;
corebit_term corebit_term_inst10 (
    .in(corebit_term_inst10_in)
);
assign corebit_term_inst11_in = I3_4_B;
corebit_term corebit_term_inst11 (
    .in(corebit_term_inst11_in)
);
assign corebit_term_inst12_in = I3_4_C;
corebit_term corebit_term_inst12 (
    .in(corebit_term_inst12_in)
);
assign corebit_term_inst2_in = I2_C;
corebit_term corebit_term_inst2 (
    .in(corebit_term_inst2_in)
);
assign corebit_term_inst3_in = I3_0_B;
corebit_term corebit_term_inst3 (
    .in(corebit_term_inst3_in)
);
assign corebit_term_inst4_in = I3_0_C;
corebit_term corebit_term_inst4 (
    .in(corebit_term_inst4_in)
);
assign corebit_term_inst5_in = I3_1_B;
corebit_term corebit_term_inst5 (
    .in(corebit_term_inst5_in)
);
assign corebit_term_inst6_in = I3_1_C;
corebit_term corebit_term_inst6 (
    .in(corebit_term_inst6_in)
);
assign corebit_term_inst7_in = I3_2_B;
corebit_term corebit_term_inst7 (
    .in(corebit_term_inst7_in)
);
assign corebit_term_inst8_in = I3_2_C;
corebit_term corebit_term_inst8 (
    .in(corebit_term_inst8_in)
);
assign corebit_term_inst9_in = I3_3_B;
corebit_term corebit_term_inst9 (
    .in(corebit_term_inst9_in)
);
assign term_inst0_in = I1;
coreir_term #(
    .width(5)
) term_inst0 (
    .in(term_inst0_in)
);
endmodule

