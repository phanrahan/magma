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
corebit_term corebit_term_inst0 (
    .in(I0)
);
corebit_term corebit_term_inst1 (
    .in(I2_B)
);
corebit_term corebit_term_inst10 (
    .in(I3_3_C)
);
corebit_term corebit_term_inst11 (
    .in(I3_4_B)
);
corebit_term corebit_term_inst12 (
    .in(I3_4_C)
);
corebit_term corebit_term_inst2 (
    .in(I2_C)
);
corebit_term corebit_term_inst3 (
    .in(I3_0_B)
);
corebit_term corebit_term_inst4 (
    .in(I3_0_C)
);
corebit_term corebit_term_inst5 (
    .in(I3_1_B)
);
corebit_term corebit_term_inst6 (
    .in(I3_1_C)
);
corebit_term corebit_term_inst7 (
    .in(I3_2_B)
);
corebit_term corebit_term_inst8 (
    .in(I3_2_C)
);
corebit_term corebit_term_inst9 (
    .in(I3_3_B)
);
coreir_term #(
    .width(5)
) term_inst0 (
    .in(I1)
);
endmodule

