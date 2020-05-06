// Module `PRWDWUWSWCDGH_V` defined externally
module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module Top (
    inout pad
);
wire PRWDWUWSWCDGH_V_inst0_C;
wire PRWDWUWSWCDGH_V_inst0_PAD;
wire bit_const_0_None_out;
PRWDWUWSWCDGH_V PRWDWUWSWCDGH_V_inst0 (
    .C(PRWDWUWSWCDGH_V_inst0_C),
    .DS0(bit_const_0_None_out),
    .DS1(bit_const_0_None_out),
    .DS2(bit_const_0_None_out),
    .I(bit_const_0_None_out),
    .IE(bit_const_0_None_out),
    .OEN(bit_const_0_None_out),
    .PAD(PRWDWUWSWCDGH_V_inst0_PAD),
    .PU(bit_const_0_None_out),
    .PD(bit_const_0_None_out),
    .ST(bit_const_0_None_out),
    .SL(bit_const_0_None_out),
    .RTE(bit_const_0_None_out)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
assign PRWDWUWSWCDGH_V_inst0_PAD = pad;
endmodule

