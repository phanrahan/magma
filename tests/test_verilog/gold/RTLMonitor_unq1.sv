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

module RTLMonitor_unq1 (
    input CLK,
    input handshake_arr_0_ready,
    input handshake_arr_0_valid,
    input handshake_arr_1_ready,
    input handshake_arr_1_valid,
    input handshake_arr_2_ready,
    input handshake_arr_2_valid,
    input handshake_ready,
    input handshake_valid,
    input [4:0] in1,
    input [4:0] in2,
    input intermediate_tuple__0,
    input intermediate_tuple__1,
    input mon_temp1,
    input mon_temp2,
    input out
);
wire _magma_inline_wire0;
wire [4:0] _magma_inline_wire1;
wire [4:0] _magma_inline_wire2;
wire [4:0] arr_2d_0;
wire [4:0] arr_2d_1;

logic temp1, temp2;
logic temp3;
assign temp1 = |(in1);
assign temp2 = &(in1) & intermediate_tuple__0;
assign temp3 = temp1 ^ temp2 & _magma_inline_wire0;
assert property (@(posedge CLK) handshake_valid -> out === temp1 && temp2);
logic [4:0] temp4 [1:0];
assign temp4 = '{_magma_inline_wire1, _magma_inline_wire2};
                                   
assign _magma_inline_wire0 = arr_2d_0[1];
assign _magma_inline_wire1 = arr_2d_1;
assign _magma_inline_wire2 = arr_2d_0;
assign arr_2d_0 = in1;
assign arr_2d_1 = in2;
corebit_term corebit_term_inst0 (
    .in(_magma_inline_wire0)
);
coreir_term #(
    .width(5)
) term_inst0 (
    .in(_magma_inline_wire1)
);
coreir_term #(
    .width(5)
) term_inst1 (
    .in(_magma_inline_wire2)
);
endmodule


bind RTL_unq1 RTLMonitor_unq1 RTLMonitor_unq1_inst (
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
    .mon_temp1(orr_5_inst0_O),
    .mon_temp2(andr_5_inst0_O),
    .intermediate_tuple__0(orr_5_inst0_O),
    .intermediate_tuple__1(andr_5_inst0_O)
);