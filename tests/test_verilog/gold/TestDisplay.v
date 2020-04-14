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

module InlineVerilog0c5113eb45faf7edfd5e3603642bd052_O_I_CLK_CE (
    input __magma_inline_value_0,
    input __magma_inline_value_1,
    input __magma_inline_value_2,
    input __magma_inline_value_3
);
wire coreir_wrapInClock_inst0_out;
corebit_term corebit_term_inst0 (
    .in(__magma_inline_value_0)
);
corebit_term corebit_term_inst1 (
    .in(__magma_inline_value_1)
);
corebit_term corebit_term_inst2 (
    .in(coreir_wrapInClock_inst0_out)
);
corebit_term corebit_term_inst3 (
    .in(__magma_inline_value_3)
);
coreir_wrap coreir_wrapInClock_inst0 (
    .in(__magma_inline_value_2),
    .out(coreir_wrapInClock_inst0_out)
);
always @(posedge __magma_inline_value_2) begin
    if (__magma_inline_value_3) $display("%0t: ff.O=%d, ff.I=%d", $time, __magma_inline_value_0, __magma_inline_value_1);
end

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
FF FF_inst0 (
    .I(I),
    .O(O),
    .CLK(CLK),
    .CE(CE)
);
InlineVerilog0c5113eb45faf7edfd5e3603642bd052_O_I_CLK_CE InlineVerilog0c5113eb45faf7edfd5e3603642bd052_O_I_CLK_CE_inst0 (
    .__magma_inline_value_0(O),
    .__magma_inline_value_1(I),
    .__magma_inline_value_2(CLK),
    .__magma_inline_value_3(CE)
);
endmodule

