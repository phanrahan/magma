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
    output v0,
    input v1
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
assign v0 = corebit_undriven_inst0_out;
// @m.inline_combinational2
// def logic(self):
//     if self.io.I:
//         self.io.O @= 0
//     else:
//         self.io.O @= 1
endmodule

module Foo (
    input I,
    output O
);
wire InlineCombWrapper_inst0_v0;
InlineCombWrapper InlineCombWrapper_inst0 (
    .v0(InlineCombWrapper_inst0_v0),
    .v1(I)
);
assign O = InlineCombWrapper_inst0_v0;
endmodule

