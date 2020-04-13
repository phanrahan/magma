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
wire __magma_inline_value_1;
wire __magma_inline_value_2;
wire [3:0] __magma_inline_value_3;
wire [3:0] __magma_inline_value_4;
wire __magma_inline_value_5;
wire [3:0] arr_2d_0;
wire [3:0] arr_2d_1;
assign __magma_inline_value_1 = intermediate_tuple__0;
assign __magma_inline_value_2 = arr_2d_0[1];
assign __magma_inline_value_3 = arr_2d_1;
assign __magma_inline_value_4 = arr_2d_0;
assign __magma_inline_value_5 = handshake_valid;
assign arr_2d_0 = in1;
assign arr_2d_1 = in2;
corebit_term corebit_term_inst0 (
    .in(__magma_inline_value_1)
);
corebit_term corebit_term_inst1 (
    .in(__magma_inline_value_2)
);
corebit_term corebit_term_inst2 (
    .in(__magma_inline_value_5)
);
coreir_term #(
    .width(4)
) term_inst0 (
    .in(__magma_inline_value_3)
);
coreir_term #(
    .width(4)
) term_inst1 (
    .in(__magma_inline_value_4)
);

logic temp1, temp2;
logic temp3;
assign temp1 = |(in1);
assign temp2 = &(in1) & __magma_inline_value_1;
assign temp3 = temp1 ^ temp2 & __magma_inline_value_2;
assert property (@(posedge CLK) __magma_inline_value_5 -> out === temp1 && temp2);
logic [3:0] temp4 [1:0];
assign temp4 = '{__magma_inline_value_3, __magma_inline_value_4};
                                   
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
    .mon_temp1(orr_4_inst0.O),
    .mon_temp2(andr_4_inst0.O),
    .intermediate_tuple__0(orr_4_inst0.O),
    .intermediate_tuple__1(andr_4_inst0.O)
);