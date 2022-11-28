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
    input CLK,
    input RESETN
);
wire coreir_wrapInClock_inst0_out;
wire coreir_wrapOutClock_inst0_out;
wire temp0_O;
wire temp1_out;
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
always @(posedge CLK) disable iff (! RESETN) $display("Hello");
endmodule

