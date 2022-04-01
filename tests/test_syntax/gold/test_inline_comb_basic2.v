module corebit_undriven (
    output out
);

endmodule

module corebit_term (
    input in
);

endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module InlineCombWrapper (
    input v0,
    output v1
);
wire bit_const_0_None_out;
wire corebit_undriven_inst0_out;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
corebit_undriven corebit_undriven_inst0 (
    .out(corebit_undriven_inst0_out)
);
assign v1 = corebit_undriven_inst0_out;
// @m.inline_combinational2
// def logic(cls):
//     if cls.io.I:
//         cls.io.O @= 0
//     else:
//         cls.io.O @= 1
endmodule

module Foo (
    input I,
    output O
);
wire InlineCombWrapper_inst0_v1;
InlineCombWrapper InlineCombWrapper_inst0 (
    .v0(I),
    .v1(InlineCombWrapper_inst0_v1)
);
assign O = InlineCombWrapper_inst0_v1;
endmodule

