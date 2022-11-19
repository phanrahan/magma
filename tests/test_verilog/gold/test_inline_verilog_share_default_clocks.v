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
    input y,
    input CLK,
    input RESET
);
wire _magma_inline_wire0_O;
wire _magma_inline_wire1;
wire _magma_inline_wire2;
wire _magma_inline_wire3;
wire clk_O;
wire rst;
WireClock _magma_inline_wire0 (
    .I(clk_O),
    .O(_magma_inline_wire0_O)
);
assign _magma_inline_wire1 = rst;
assign _magma_inline_wire2 = x;
assign _magma_inline_wire3 = y;
WireClock clk (
    .I(CLK),
    .O(clk_O)
);
assign rst = RESET;

assert property (@(posedge _magma_inline_wire0_O) disable iff (! _magma_inline_wire1) _magma_inline_wire2 |-> ##1 _magma_inline_wire3);


assert property (@(posedge _magma_inline_wire0_O) disable iff (! _magma_inline_wire1) _magma_inline_wire2 |-> ##1 _magma_inline_wire3);

endmodule

