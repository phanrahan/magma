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
wire FF_inst0_O;
wire __magma_inline_value_6_out;
wire __magma_inline_value_7_out;
wire __magma_inline_value_8_out;
wire __magma_inline_value_9_out;
wire coreir_wrapInClock_inst0_out;
FF FF_inst0 (
    .I(I),
    .O(FF_inst0_O),
    .CLK(CLK),
    .CE(CE)
);
corebit_wire __magma_inline_value_6 (
    .in(FF_inst0_O),
    .out(__magma_inline_value_6_out)
);
corebit_wire __magma_inline_value_7 (
    .in(I),
    .out(__magma_inline_value_7_out)
);
corebit_wire __magma_inline_value_8 (
    .in(coreir_wrapInClock_inst0_out),
    .out(__magma_inline_value_8_out)
);
corebit_wire __magma_inline_value_9 (
    .in(CE),
    .out(__magma_inline_value_9_out)
);
corebit_term corebit_term_inst0 (
    .in(__magma_inline_value_6_out)
);
corebit_term corebit_term_inst1 (
    .in(__magma_inline_value_7_out)
);
corebit_term corebit_term_inst2 (
    .in(__magma_inline_value_8_out)
);
corebit_term corebit_term_inst3 (
    .in(__magma_inline_value_9_out)
);
coreir_wrap coreir_wrapInClock_inst0 (
    .in(CLK),
    .out(coreir_wrapInClock_inst0_out)
);
assign O = FF_inst0_O;
always @(posedge __magma_inline_value_8_out) begin
    if (__magma_inline_value_9_out) $display("%0t: ff.O=%d, ff.I=%d", $time, __magma_inline_value_6_out, __magma_inline_value_7_out);
end

endmodule

