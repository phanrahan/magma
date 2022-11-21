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

module WireClock (
    input I,
    output O
);
wire Wire_inst0_out;
wire coreir_wrapInClock_inst0_out;
wire coreir_wrapOutClock_inst0_out;
corebit_wire Wire_inst0 (
    .in(coreir_wrapInClock_inst0_out),
    .out(Wire_inst0_out)
);
coreir_wrap coreir_wrapInClock_inst0 (
    .in(I),
    .out(coreir_wrapInClock_inst0_out)
);
coreir_wrap coreir_wrapOutClock_inst0 (
    .in(Wire_inst0_out),
    .out(coreir_wrapOutClock_inst0_out)
);
assign O = coreir_wrapOutClock_inst0_out;
endmodule

module Bar (
    input CLK,
    input RESETN
);
wire _magma_inline_wire0_O;
wire _magma_inline_wire1_out;
wire coreir_wrapInClock_inst0_out;
wire coreir_wrapOutClock_inst0_out;
wire temp0_O;
wire temp1_out;
wire temp2_O;
wire temp3_out;
WireClock _magma_inline_wire0 (
    .I(temp2_O),
    .O(_magma_inline_wire0_O)
);
corebit_wire _magma_inline_wire1 (
    .in(temp3_out),
    .out(_magma_inline_wire1_out)
);
coreir_wrap coreir_wrapInClock_inst0 (
    .in(temp0_O),
    .out(coreir_wrapInClock_inst0_out)
);
coreir_wrap coreir_wrapOutClock_inst0 (
    .in(temp1_out),
    .out(coreir_wrapOutClock_inst0_out)
);
Foo foo0 (
    .CLK(coreir_wrapOutClock_inst0_out)
);
WireClock temp0 (
    .I(CLK),
    .O(temp0_O)
);
corebit_wire temp1 (
    .in(coreir_wrapInClock_inst0_out),
    .out(temp1_out)
);
WireClock temp2 (
    .I(CLK),
    .O(temp2_O)
);
corebit_wire temp3 (
    .in(RESETN),
    .out(temp3_out)
);
always @(posedge _magma_inline_wire0_O) disable iff (! _magma_inline_wire1_out) $display("Hello");
endmodule

