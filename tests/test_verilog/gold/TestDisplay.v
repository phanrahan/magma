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

module FF(input I, output reg O, input CLK, input CE);
always @(posedge CLK) begin
  if (CE) O <= I;
end
endmodule
module TestDisplay (
    input I,
    output O,
    input CLK,
    input CE
);
wire _magma_inline_wire0;
wire _magma_inline_wire1;
wire _magma_inline_wire2_O;
wire _magma_inline_wire3;
FF FF_inst0 (
    .I(I),
    .O(O),
    .CLK(CLK),
    .CE(CE)
);
assign _magma_inline_wire0 = O;
assign _magma_inline_wire1 = I;
WireClock _magma_inline_wire2 (
    .I(CLK),
    .O(_magma_inline_wire2_O)
);
assign _magma_inline_wire3 = CE;
always @(posedge _magma_inline_wire2_O) begin
    if (_magma_inline_wire3) $display("%0t: ff.O=%d, ff.I=%d", $time, _magma_inline_wire0, _magma_inline_wire1);
end

endmodule

