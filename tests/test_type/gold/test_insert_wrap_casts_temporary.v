// Module `Foo` defined externally
module coreir_wrap (
    input in,
    output out
);
  assign out = in;
endmodule

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

module Bar (
    input CLK
);
wire _magma_inline_wire0_out;
wire coreir_wrapInClock_inst0_out;
wire coreir_wrapInClock_inst1_out;
wire coreir_wrapOutClock_inst0_out;
wire coreir_wrapOutClock_inst1_out;
wire temp1_out;
Foo Foo_inst0 (
    .CLK(coreir_wrapOutClock_inst0_out)
);
corebit_wire _magma_inline_wire0 (
    .in(coreir_wrapInClock_inst0_out),
    .out(_magma_inline_wire0_out)
);
coreir_wrap coreir_wrapInClock_inst0 (
    .in(CLK),
    .out(coreir_wrapInClock_inst0_out)
);
coreir_wrap coreir_wrapInClock_inst1 (
    .in(CLK),
    .out(coreir_wrapInClock_inst1_out)
);
coreir_wrap coreir_wrapOutClock_inst0 (
    .in(temp1_out),
    .out(coreir_wrapOutClock_inst0_out)
);
coreir_wrap coreir_wrapOutClock_inst1 (
    .in(_magma_inline_wire0_out),
    .out(coreir_wrapOutClock_inst1_out)
);
corebit_wire temp1 (
    .in(coreir_wrapInClock_inst1_out),
    .out(temp1_out)
);
always @(posedge coreir_wrapOutClock_inst1_out) $display("Hello");
endmodule

