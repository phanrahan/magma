module corebit_wire (
    input in,
    output out
);
  assign out = in;
endmodule

module corebit_term (
    input in
);

endmodule

module Foo_unq1 (
    input I
);
wire _magma_inline_wire0_out;
corebit_wire _magma_inline_wire0 (
    .in(I),
    .out(_magma_inline_wire0_out)
);
always @(*) $display("%x\n", _magma_inline_wire0_out);
endmodule

module Foo (
    input I
);
wire _magma_inline_wire0_out;
corebit_wire _magma_inline_wire0 (
    .in(I),
    .out(_magma_inline_wire0_out)
);
always @(*) $display("%d\n", _magma_inline_wire0_out);
endmodule

module Top (
    input I
);
Foo Foo_inst0 (
    .I(I)
);
Foo_unq1 Foo_inst1 (
    .I(I)
);
endmodule

