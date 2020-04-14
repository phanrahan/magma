module coreir_wrap (
    input in,
    output out
);
  assign out = in;
endmodule

module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module corebit_term (
    input in
);

endmodule

module InlineVeriloge46c6d340f1dcb5f904b568baa9feee2_in1_in1_RTLMonitor_intermediate_tuple_0_RTLMonitor_in1_1_CLK_out_in2_in1_RTLMonitor_handshake_valid (
    input [3:0] __magma_inline_value_0,
    input [3:0] __magma_inline_value_1,
    input __magma_inline_value_2,
    input __magma_inline_value_3,
    input __magma_inline_value_4,
    input __magma_inline_value_5,
    input [3:0] __magma_inline_value_6,
    input [3:0] __magma_inline_value_7,
    input __magma_inline_value_8
);
wire coreir_wrapInClock_inst0_out;
corebit_term corebit_term_inst0 (
    .in(__magma_inline_value_2)
);
corebit_term corebit_term_inst1 (
    .in(__magma_inline_value_3)
);
corebit_term corebit_term_inst2 (
    .in(coreir_wrapInClock_inst0_out)
);
corebit_term corebit_term_inst3 (
    .in(__magma_inline_value_5)
);
corebit_term corebit_term_inst4 (
    .in(__magma_inline_value_8)
);
coreir_wrap coreir_wrapInClock_inst0 (
    .in(__magma_inline_value_4),
    .out(coreir_wrapInClock_inst0_out)
);
coreir_term #(
    .width(4)
) term_inst0 (
    .in(__magma_inline_value_0)
);
coreir_term #(
    .width(4)
) term_inst1 (
    .in(__magma_inline_value_1)
);
coreir_term #(
    .width(4)
) term_inst2 (
    .in(__magma_inline_value_6)
);
coreir_term #(
    .width(4)
) term_inst3 (
    .in(__magma_inline_value_7)
);

logic temp1, temp2;
logic temp3;
assign temp1 = |(__magma_inline_value_0);
assign temp2 = &(__magma_inline_value_0) & __magma_inline_value_2;
assign temp3 = temp1 ^ temp2 & __magma_inline_value_3;
assert property (@(posedge __magma_inline_value_4) __magma_inline_value_8 -> __magma_inline_value_5 === temp1 && temp2);
logic [3:0] temp4 [1:0];
assign temp4 = '{__magma_inline_value_6, __magma_inline_value_7};
                                   
endmodule

module RTLMonitor (
    input CLK,
    input handshake_arr_0_ready,
    input handshake_arr_0_valid,
    input handshake_arr_1_ready,
    input handshake_arr_1_valid,
    input handshake_arr_2_ready,
    input handshake_arr_2_valid,
    input handshake_ready,
    input handshake_valid,
    input [3:0] in1,
    input [3:0] in2,
    input intermediate_tuple__0,
    input intermediate_tuple__1,
    input mon_temp1,
    input mon_temp2,
    input out
);
InlineVeriloge46c6d340f1dcb5f904b568baa9feee2_in1_in1_RTLMonitor_intermediate_tuple_0_RTLMonitor_in1_1_CLK_out_in2_in1_RTLMonitor_handshake_valid InlineVeriloge46c6d340f1dcb5f904b568baa9feee2_in1_in1_RTLMonitor_intermediate_tuple_0_RTLMonitor_in1_1_CLK_out_in2_in1_RTLMonitor_handshake_valid_inst0 (
    .__magma_inline_value_0(in1),
    .__magma_inline_value_1(in1),
    .__magma_inline_value_2(intermediate_tuple__0),
    .__magma_inline_value_3(in1[1]),
    .__magma_inline_value_4(CLK),
    .__magma_inline_value_5(out),
    .__magma_inline_value_6(in2),
    .__magma_inline_value_7(in1),
    .__magma_inline_value_8(handshake_valid)
);
endmodule


bind RTL RTLMonitor RTLMonitor_inst (
    .CLK(CLK),
    .in1(in1),
    .in2(in2),
    .out(out),
    .handshake_ready(handshake_ready),
    .handshake_valid(handshake_valid),
    .handshake_arr_0_ready(handshake_arr_0_ready),
    .handshake_arr_0_valid(handshake_arr_0_valid),
    .handshake_arr_1_ready(handshake_arr_1_ready),
    .handshake_arr_1_valid(handshake_arr_1_valid),
    .handshake_arr_2_ready(handshake_arr_2_ready),
    .handshake_arr_2_valid(handshake_arr_2_valid),
    .mon_temp1(orr_4_inst0_O),
    .mon_temp2(andr_4_inst0_O),
    .intermediate_tuple__0(orr_4_inst0_O),
    .intermediate_tuple__1(andr_4_inst0_O)
);