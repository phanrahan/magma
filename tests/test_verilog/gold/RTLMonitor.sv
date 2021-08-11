module bar_coreir_wrap (
    input in,
    output out
);
  assign out = in;
endmodule

module bar_coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module bar_foo_WireClock (
    input I,
    output O
);
wire Wire_inst0;
wire coreir_wrapInClock_inst0_out;
assign Wire_inst0 = coreir_wrapInClock_inst0_out;
bar_coreir_wrap coreir_wrapInClock_inst0 (
    .in(I),
    .out(coreir_wrapInClock_inst0_out)
);
bar_coreir_wrap coreir_wrapOutClock_inst0 (
    .in(Wire_inst0),
    .out(O)
);
endmodule

module bar_corebit_term (
    input in
);

endmodule

module bar_foo_RTLMonitor (
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
    input [3:0] inst_input,
    input [2:0] intermediate_ndarr [1:0],
    input intermediate_tuple__0,
    input intermediate_tuple__1,
    input mon_temp1,
    input mon_temp2,
    input mon_temp3,
    input [1:0] ndarr [2:0],
    input out,
    input [19:0] tuple_arr [0:0]
);
wire [3:0] _magma_inline_wire0;
wire _magma_inline_wire1;
wire _magma_inline_wire10;
wire _magma_inline_wire2;
wire _magma_inline_wire3_O;
wire _magma_inline_wire4;
wire [3:0] _magma_inline_wire5;
wire [3:0] _magma_inline_wire6;
wire [3:0] _magma_inline_wire7;
wire _magma_inline_wire8;
wire _magma_inline_wire9;
wire [3:0] arr_2d_0;
wire [3:0] arr_2d_1;
assign _magma_inline_wire0 = in1;
assign _magma_inline_wire1 = intermediate_tuple__0;
assign _magma_inline_wire10 = handshake_valid;
assign _magma_inline_wire2 = arr_2d_0[1];
bar_foo_WireClock _magma_inline_wire3 (
    .I(CLK),
    .O(_magma_inline_wire3_O)
);
assign _magma_inline_wire4 = out;
assign _magma_inline_wire5 = arr_2d_1;
assign _magma_inline_wire6 = arr_2d_0;
assign _magma_inline_wire7 = inst_input;
assign _magma_inline_wire8 = mon_temp3;
assign _magma_inline_wire9 = intermediate_ndarr[1][1];
assign arr_2d_0 = in1;
assign arr_2d_1 = in2;

logic temp1, temp2;
logic temp3;
assign temp1 = |(_magma_inline_wire0);
assign temp2 = &(_magma_inline_wire0) & _magma_inline_wire1;
assign temp3 = temp1 ^ temp2 & _magma_inline_wire2;
assert property (@(posedge _magma_inline_wire3_O) _magma_inline_wire10 -> _magma_inline_wire4 === temp1 && temp2);
logic [3:0] temp4 [1:0];
assign temp4 = '{_magma_inline_wire5, _magma_inline_wire6};
always @(*) $display("%x", _magma_inline_wire7 & {4{_magma_inline_wire8}});
logic temp5;
assign temp5 = _magma_inline_wire9;
                                   
endmodule



`ifdef BIND_ON
bind bar_foo_RTL bar_foo_RTLMonitor bar_foo_RTLMonitor_inst (
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
    .ndarr(ndarr),
    .mon_temp1(_magma_bind_wire_0),
    .mon_temp2(_magma_bind_wire_1),
    .intermediate_tuple__0(_magma_bind_wire_2_0),
    .intermediate_tuple__1(_magma_bind_wire_2_1),
    .inst_input(_magma_bind_wire_3),
    .mon_temp3(_magma_bind_wire_4),
    .intermediate_ndarr('{_magma_bind_wire_5_1, _magma_bind_wire_5_0}),
    .tuple_arr('{nested_other_circ._magma_bind_wire_0_0})
);
`endif
