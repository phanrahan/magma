module corebit_term (
    input in
);

endmodule

module InlineVerilogfaa1fa843bd1308fe1bf206135040be9___magma_inline_value_0_Main_arr_0___magma_inline_value_1_Main_arr_1 (
    input __magma_inline_value_0,
    input __magma_inline_value_1
);
corebit_term corebit_term_inst0 (
    .in(__magma_inline_value_0)
);
corebit_term corebit_term_inst1 (
    .in(__magma_inline_value_1)
);

assert property (@(posedge CLK) __magma_inline_value_0 |-> ##1 __magma_inline_value_1);

endmodule

module InlineVerilogce13f27aea30971e187e631b7bd2d907___magma_inline_value_0_O___magma_inline_value_1_I (
    input __magma_inline_value_0,
    input __magma_inline_value_1
);
corebit_term corebit_term_inst0 (
    .in(__magma_inline_value_0)
);
corebit_term corebit_term_inst1 (
    .in(__magma_inline_value_1)
);

assert property (@(posedge CLK) __magma_inline_value_1 |-> ##1 __magma_inline_value_0);

endmodule

module FF(input I, output reg O, input CLK);
always @(posedge CLK) begin
  O <= I;
end
endmodule
module Main (
    input I,
    output O,
    input [1:0] arr,
    input CLK
);
FF FF_inst0 (
    .I(I),
    .O(O),
    .CLK(CLK)
);
InlineVerilogce13f27aea30971e187e631b7bd2d907___magma_inline_value_0_O___magma_inline_value_1_I InlineVerilogce13f27aea30971e187e631b7bd2d907___magma_inline_value_0_O___magma_inline_value_1_I_inst0 (
    .__magma_inline_value_0(O),
    .__magma_inline_value_1(I)
);
InlineVerilogfaa1fa843bd1308fe1bf206135040be9___magma_inline_value_0_Main_arr_0___magma_inline_value_1_Main_arr_1 InlineVerilogfaa1fa843bd1308fe1bf206135040be9___magma_inline_value_0_Main_arr_0___magma_inline_value_1_Main_arr_1_inst0 (
    .__magma_inline_value_0(arr[0]),
    .__magma_inline_value_1(arr[1])
);
endmodule

