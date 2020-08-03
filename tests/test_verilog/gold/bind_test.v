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
wire [3:0] term_inst0_in;
assign term_inst0_in = I;
coreir_term #(
    .width(4)
) term_inst0 (
    .in(term_inst0_in)
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
wire [3:0] SomeCircuit_inst0_I;
wire _magma_bind_wire_0;
wire _magma_bind_wire_1;
wire _magma_bind_wire_2_0;
wire _magma_bind_wire_2_1;
wire [3:0] _magma_bind_wire_3;
wire [3:0] andr_4_inst0_I;
wire andr_4_inst0_O;
wire corebit_term_inst0_in;
wire corebit_term_inst1_in;
wire corebit_term_inst2_in;
wire corebit_term_inst3_in;
wire logical_and_inst0_I0;
wire logical_and_inst0_I1;
wire [3:0] magma_Bits_4_xor_inst0_out;
wire [3:0] orr_4_inst0_I;
wire orr_4_inst0_O;
wire [3:0] term_inst0_in;
assign SomeCircuit_inst0_I = magma_Bits_4_xor_inst0_out;
SomeCircuit SomeCircuit_inst0 (
    .I(SomeCircuit_inst0_I)
);
assign _magma_bind_wire_0 = orr_4_inst0_O;
assign _magma_bind_wire_1 = andr_4_inst0_O;
assign _magma_bind_wire_2_0 = orr_4_inst0_O;
assign _magma_bind_wire_2_1 = andr_4_inst0_O;
assign _magma_bind_wire_3 = magma_Bits_4_xor_inst0_out;
assign andr_4_inst0_I = in1;
andr_4 andr_4_inst0 (
    .I(andr_4_inst0_I),
    .O(andr_4_inst0_O)
);
assign corebit_term_inst0_in = _magma_bind_wire_0;
corebit_term corebit_term_inst0 (
    .in(corebit_term_inst0_in)
);
assign corebit_term_inst1_in = _magma_bind_wire_1;
corebit_term corebit_term_inst1 (
    .in(corebit_term_inst1_in)
);
assign corebit_term_inst2_in = _magma_bind_wire_2_0;
corebit_term corebit_term_inst2 (
    .in(corebit_term_inst2_in)
);
assign corebit_term_inst3_in = _magma_bind_wire_2_1;
corebit_term corebit_term_inst3 (
    .in(corebit_term_inst3_in)
);
assign logical_and_inst0_I0 = orr_4_inst0_O;
assign logical_and_inst0_I1 = andr_4_inst0_O;
logical_and logical_and_inst0 (
    .I0(logical_and_inst0_I0),
    .I1(logical_and_inst0_I1),
    .O(out)
);
assign magma_Bits_4_xor_inst0_out = in1 ^ in2;
assign orr_4_inst0_I = in1;
orr_4 orr_4_inst0 (
    .I(orr_4_inst0_I),
    .O(orr_4_inst0_O)
);
assign term_inst0_in = _magma_bind_wire_3;
coreir_term #(
    .width(4)
) term_inst0 (
    .in(term_inst0_in)
);
assign handshake_arr_0_valid = handshake_arr_2_ready;
assign handshake_arr_1_valid = handshake_arr_1_ready;
assign handshake_arr_2_valid = handshake_arr_0_ready;
assign handshake_valid = handshake_ready;
endmodule

