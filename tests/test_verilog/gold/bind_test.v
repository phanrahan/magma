            module orr_4 (input [3:0] I, output O);
            assign O = |(I);
            endmodule
            module logical_and (input I0, input I1, output O);
            assign O = I0 && I1;
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

            module andr_4 (input [3:0] I, output O);
            assign O = &(I);
            endmodule
module SomeCircuit (
    input [3:0] I
);
coreir_term #(
    .width(4)
) term_inst0 (
    .in(I)
);
endmodule

module RTL (
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
    output out
);
wire _magma_bind_wire_0;
wire _magma_bind_wire_1;
wire [3:0] _magma_bind_wire_2;
wire andr_4_inst0_O;
wire [3:0] magma_Bits_4_xor_inst0_out;
wire orr_4_inst0_O;
SomeCircuit SomeCircuit_inst0 (
    .I(magma_Bits_4_xor_inst0_out)
);
assign _magma_bind_wire_0 = orr_4_inst0_O;
assign _magma_bind_wire_1 = andr_4_inst0_O;
assign _magma_bind_wire_2 = magma_Bits_4_xor_inst0_out;
andr_4 andr_4_inst0 (
    .I(in1),
    .O(andr_4_inst0_O)
);
corebit_term corebit_term_inst0 (
    .in(_magma_bind_wire_0)
);
corebit_term corebit_term_inst1 (
    .in(_magma_bind_wire_1)
);
logical_and logical_and_inst0 (
    .I0(orr_4_inst0_O),
    .I1(andr_4_inst0_O),
    .O(out)
);
assign magma_Bits_4_xor_inst0_out = in1 ^ in2;
orr_4 orr_4_inst0 (
    .I(in1),
    .O(orr_4_inst0_O)
);
coreir_term #(
    .width(4)
) term_inst0 (
    .in(_magma_bind_wire_2)
);
assign handshake_arr_0_valid = handshake_arr_2_ready;
assign handshake_arr_1_valid = handshake_arr_1_ready;
assign handshake_arr_2_valid = handshake_arr_0_ready;
assign handshake_valid = handshake_ready;
endmodule

