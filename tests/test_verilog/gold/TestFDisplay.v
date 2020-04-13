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
module TestFDisplay (
    input I,
    output O,
    input CLK,
    input CE
);
wire FF_inst0_O;
wire __magma_inline_value_10_out;
wire __magma_inline_value_11_out;
wire __magma_inline_value_12_out;
wire __magma_inline_value_13_out;
wire coreir_wrapInClock_inst0_out;
FF FF_inst0 (
    .I(I),
    .O(FF_inst0_O),
    .CLK(CLK),
    .CE(CE)
);
corebit_wire __magma_inline_value_10 (
    .in(FF_inst0_O),
    .out(__magma_inline_value_10_out)
);
corebit_wire __magma_inline_value_11 (
    .in(I),
    .out(__magma_inline_value_11_out)
);
corebit_wire __magma_inline_value_12 (
    .in(coreir_wrapInClock_inst0_out),
    .out(__magma_inline_value_12_out)
);
corebit_wire __magma_inline_value_13 (
    .in(CE),
    .out(__magma_inline_value_13_out)
);
corebit_term corebit_term_inst0 (
    .in(__magma_inline_value_10_out)
);
corebit_term corebit_term_inst1 (
    .in(__magma_inline_value_11_out)
);
corebit_term corebit_term_inst2 (
    .in(__magma_inline_value_12_out)
);
corebit_term corebit_term_inst3 (
    .in(__magma_inline_value_13_out)
);
coreir_wrap coreir_wrapInClock_inst0 (
    .in(CLK),
    .out(coreir_wrapInClock_inst0_out)
);
assign O = FF_inst0_O;

integer \_file_test_fdisplay.log ;
initial \_file_test_fdisplay.log = $fopen("test_fdisplay.log", "a");


always @(posedge __magma_inline_value_12_out) begin
    if (__magma_inline_value_13_out) $fdisplay(\_file_test_fdisplay.log , "ff.O=%d, ff.I=%d", __magma_inline_value_10_out, __magma_inline_value_11_out);
end



final $fclose(\_file_test_fdisplay.log );

endmodule

