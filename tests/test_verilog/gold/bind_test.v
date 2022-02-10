// Module `foo_OtherCircuit` defined externally
module orr_4 (input [3:0] I, output O);
assign O = |(I);
endmodule
module logical_and (input I0, input I1, output O);
assign O = I0 && I1;
endmodule
module andr_4 (input [3:0] I, output O);
assign O = &(I);
endmodule
module bar_coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module bar_foo_SomeCircuit (
    input [3:0] I
);
bar_coreir_term #(
    .width(4)
) term_inst0 (
    .in(I)
);
endmodule

module bar_foo_NestedOtherCircuit (
    output [19:0] x_y [0:0]
);
wire [19:0] _magma_bind_wire_0_0;
assign _magma_bind_wire_0_0 = x_y[0];
foo_OtherCircuit other_circ (
    .x_y(x_y)
);
bar_coreir_term #(
    .width(20)
) term_inst0 (
    .in(_magma_bind_wire_0_0)
);
endmodule

module bar_corebit_term (
    input in
);

endmodule

module bar_foo_RTL (
    input CLK,
    input handshake_arr_0_ready,
    output handshake_arr_0_valid,
    input handshake_arr_1_ready,
    output handshake_arr_1_valid,
    input handshake_arr_2_ready,
    output handshake_arr_2_valid,
    input handshake_ready,
    output handshake_valid,
    input [3:0] in1,
    input [3:0] in2,
    input [1:0] ndarr [2:0],
    output out
);
wire _magma_bind_wire_0;
wire _magma_bind_wire_1;
wire _magma_bind_wire_2_0;
wire _magma_bind_wire_2_1;
wire [3:0] _magma_bind_wire_3;
wire _magma_bind_wire_4;
wire [2:0] _magma_bind_wire_5_0;
wire [2:0] _magma_bind_wire_5_1;
wire andr_4_inst0_O;
wire [2:0] intermediate_ndarr_0;
wire [2:0] intermediate_ndarr_1;
wire [3:0] magma_Bits_4_xor_inst0_out;
wire [19:0] nested_other_circ_x_y [0:0];
wire orr_4_inst0_O;
wire temp3;
bar_foo_SomeCircuit SomeCircuit_inst0 (
    .I(magma_Bits_4_xor_inst0_out)
);
assign _magma_bind_wire_0 = orr_4_inst0_O;
assign _magma_bind_wire_1 = andr_4_inst0_O;
assign _magma_bind_wire_2_0 = orr_4_inst0_O;
assign _magma_bind_wire_2_1 = andr_4_inst0_O;
assign _magma_bind_wire_3 = magma_Bits_4_xor_inst0_out;
assign _magma_bind_wire_4 = temp3;
assign _magma_bind_wire_5_0 = intermediate_ndarr_0;
assign _magma_bind_wire_5_1 = intermediate_ndarr_1;
andr_4 andr_4_inst0 (
    .I(in1),
    .O(andr_4_inst0_O)
);
bar_corebit_term corebit_term_inst0 (
    .in(temp3)
);
bar_corebit_term corebit_term_inst1 (
    .in(_magma_bind_wire_0)
);
bar_corebit_term corebit_term_inst10 (
    .in(_magma_bind_wire_5_1[1])
);
bar_corebit_term corebit_term_inst11 (
    .in(_magma_bind_wire_5_1[2])
);
bar_corebit_term corebit_term_inst2 (
    .in(_magma_bind_wire_1)
);
bar_corebit_term corebit_term_inst3 (
    .in(_magma_bind_wire_2_0)
);
bar_corebit_term corebit_term_inst4 (
    .in(_magma_bind_wire_2_1)
);
bar_corebit_term corebit_term_inst5 (
    .in(_magma_bind_wire_4)
);
bar_corebit_term corebit_term_inst6 (
    .in(_magma_bind_wire_5_0[0])
);
bar_corebit_term corebit_term_inst7 (
    .in(_magma_bind_wire_5_0[1])
);
bar_corebit_term corebit_term_inst8 (
    .in(_magma_bind_wire_5_0[2])
);
bar_corebit_term corebit_term_inst9 (
    .in(_magma_bind_wire_5_1[0])
);
assign intermediate_ndarr_0 = {ndarr[2][0],ndarr[1][0],ndarr[0][0]};
assign intermediate_ndarr_1 = {ndarr[2][1],ndarr[1][1],ndarr[0][1]};
logical_and logical_and_inst0 (
    .I0(orr_4_inst0_O),
    .I1(andr_4_inst0_O),
    .O(out)
);
assign magma_Bits_4_xor_inst0_out = in1 ^ in2;
bar_foo_NestedOtherCircuit nested_other_circ (
    .x_y(nested_other_circ_x_y)
);
orr_4 orr_4_inst0 (
    .I(in1),
    .O(orr_4_inst0_O)
);
assign temp3 = andr_4_inst0_O;
wire [5:0] term_inst0_in;
assign term_inst0_in = {ndarr[2],ndarr[1],ndarr[0]};
bar_coreir_term #(
    .width(6)
) term_inst0 (
    .in(term_inst0_in)
);
bar_coreir_term #(
    .width(4)
) term_inst1 (
    .in(_magma_bind_wire_3)
);
assign handshake_arr_0_valid = handshake_arr_2_ready;
assign handshake_arr_1_valid = handshake_arr_1_ready;
assign handshake_arr_2_valid = handshake_arr_0_ready;
assign handshake_valid = handshake_ready;
endmodule

