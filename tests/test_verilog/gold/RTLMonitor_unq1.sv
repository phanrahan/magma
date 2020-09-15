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

module foo_RTLMonitor_unq1 (
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
    input [4:0] inst_input,
    input intermediate_tuple__0,
    input intermediate_tuple__1,
    input mon_temp1,
    input mon_temp2,
    input mon_temp3,
    input out
);
wire _magma_inline_wire0;
wire [4:0] _magma_inline_wire1;
wire [4:0] _magma_inline_wire2;
wire [4:0] arr_2d_0;
wire [4:0] arr_2d_1;
assign _magma_inline_wire0 = arr_2d_0[1];
assign _magma_inline_wire1 = arr_2d_1;
assign _magma_inline_wire2 = arr_2d_0;
assign arr_2d_0 = in1;
assign arr_2d_1 = in2;

logic temp1, temp2;
logic temp3;
assign temp1 = |(in1);
assign temp2 = &(in1) & intermediate_tuple__0;
assign temp3 = temp1 ^ temp2 & _magma_inline_wire0;
assert property (@(posedge CLK) handshake_valid -> out === temp1 && temp2);
logic [4:0] temp4 [1:0];
assign temp4 = '{_magma_inline_wire1, _magma_inline_wire2};
always @(*) $display("%x", inst_input & {5{mon_temp3}});
                                   
endmodule


bind foo_RTL_unq1 foo_RTLMonitor_unq1 foo_RTLMonitor_unq1_inst (
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
    .mon_temp1(_magma_bind_wire_0),
    .mon_temp2(_magma_bind_wire_1),
    .intermediate_tuple__0(_magma_bind_wire_2_0),
    .intermediate_tuple__1(_magma_bind_wire_2_1),
    .inst_input(_magma_bind_wire_3),
    .mon_temp3(_magma_bind_wire_4)
);