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
wire clk_O;
wire rst;
WireClock clk (
    .I(CLK),
    .O(clk_O)
);
assign rst = RESET;

assert property (@(posedge clk_O) disable iff (! rst) x |-> ##1 y);


assert property (@(posedge clk_O) disable iff (! rst) x |-> ##1 y);

endmodule

