module coreir_wrap (
    input in,
    output out
);
  assign out = in;
endmodule

module corebit_term (
    input in
);

endmodule

module WireClock (
    input I,
    output O
);
wire Wire_inst0;
wire coreir_wrapInClock_inst0_out;
assign Wire_inst0 = coreir_wrapInClock_inst0_out;
coreir_wrap coreir_wrapInClock_inst0 (
    .in(I),
    .out(coreir_wrapInClock_inst0_out)
);
coreir_wrap coreir_wrapOutClock_inst0 (
    .in(Wire_inst0),
    .out(O)
);
endmodule

module Foo (
    input x,
    input y
);
wire _magma_inline_wire0_O;
wire _magma_inline_wire1_O;
WireClock _magma_inline_wire0 (
    .I(x),
    .O(_magma_inline_wire0_O)
);
WireClock _magma_inline_wire1 (
    .I(y),
    .O(_magma_inline_wire1_O)
);

Foo bar (.x(_magma_inline_wire0_O, .y_magma_inline_wire1_O))

endmodule

