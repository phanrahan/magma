module coreir_wrap (
    input in,
    output out
);
  assign out = in;
endmodule

module coreir_undriven #(
    parameter width = 1
) (
    output [width-1:0] out
);

endmodule

module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module corebit_undriven (
    output out
);

endmodule

            module orr_5 (input [4:0] I, output O);
            assign O = |(I);
            endmodule
            module orr_4 (input [3:0] I, output O);
            assign O = |(I);
            endmodule
module corebit_term (
    input in
);

endmodule

            module logical_and (input I0, input I1, output O);
            assign O = I0 && I1;
            endmodule
            module andr_5 (input [4:0] I, output O);
            assign O = &(I);
            endmodule
            module andr_4 (input [3:0] I, output O);
            assign O = &(I);
            endmodule
module SomeCircuit_unq1 (
    input [4:0] I
);
wire [4:0] term_inst0_in;
assign term_inst0_in = I;
coreir_term #(
    .width(5)
) term_inst0 (
    .in(term_inst0_in)
);
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

module RTL_unq1 (
    input CLK,
    input handshake_arr_0_ready,
    output handshake_arr_0_valid,
    input handshake_arr_1_ready,
    output handshake_arr_1_valid,
    input handshake_arr_2_ready,
    output handshake_arr_2_valid,
    input handshake_ready,
    output handshake_valid,
    input [4:0] in1,
    input [4:0] in2,
    output out
);
wire [4:0] SomeCircuit_inst0_I;
wire _magma_bind_wire_0;
wire _magma_bind_wire_1;
wire _magma_bind_wire_2_0;
wire _magma_bind_wire_2_1;
wire [4:0] _magma_bind_wire_3;
wire [4:0] andr_5_inst0_I;
wire andr_5_inst0_O;
wire corebit_term_inst0_in;
wire corebit_term_inst1_in;
wire corebit_term_inst2_in;
wire corebit_term_inst3_in;
wire corebit_term_inst4_in;
wire coreir_wrapInClock_inst0_in;
wire coreir_wrapInClock_inst0_out;
wire logical_and_inst0_I0;
wire logical_and_inst0_I1;
wire [4:0] magma_Bits_5_xor_inst0_out;
wire [4:0] orr_5_inst0_I;
wire orr_5_inst0_O;
wire [4:0] term_inst0_in;
assign SomeCircuit_inst0_I = magma_Bits_5_xor_inst0_out;
SomeCircuit_unq1 SomeCircuit_inst0 (
    .I(SomeCircuit_inst0_I)
);
assign _magma_bind_wire_0 = orr_5_inst0_O;
assign _magma_bind_wire_1 = andr_5_inst0_O;
assign _magma_bind_wire_2_0 = orr_5_inst0_O;
assign _magma_bind_wire_2_1 = andr_5_inst0_O;
assign _magma_bind_wire_3 = magma_Bits_5_xor_inst0_out;
assign andr_5_inst0_I = in1;
andr_5 andr_5_inst0 (
    .I(andr_5_inst0_I),
    .O(andr_5_inst0_O)
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
assign corebit_term_inst4_in = coreir_wrapInClock_inst0_out;
corebit_term corebit_term_inst4 (
    .in(corebit_term_inst4_in)
);
assign coreir_wrapInClock_inst0_in = CLK;
coreir_wrap coreir_wrapInClock_inst0 (
    .in(coreir_wrapInClock_inst0_in),
    .out(coreir_wrapInClock_inst0_out)
);
assign logical_and_inst0_I0 = orr_5_inst0_O;
assign logical_and_inst0_I1 = andr_5_inst0_O;
logical_and logical_and_inst0 (
    .I0(logical_and_inst0_I0),
    .I1(logical_and_inst0_I1),
    .O(out)
);
assign magma_Bits_5_xor_inst0_out = in1 ^ in2;
assign orr_5_inst0_I = in1;
orr_5 orr_5_inst0 (
    .I(orr_5_inst0_I),
    .O(orr_5_inst0_O)
);
assign term_inst0_in = _magma_bind_wire_3;
coreir_term #(
    .width(5)
) term_inst0 (
    .in(term_inst0_in)
);
assign handshake_arr_0_valid = handshake_arr_2_ready;
assign handshake_arr_1_valid = handshake_arr_1_ready;
assign handshake_arr_2_valid = handshake_arr_0_ready;
assign handshake_valid = handshake_ready;
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
wire corebit_term_inst4_in;
wire coreir_wrapInClock_inst0_in;
wire coreir_wrapInClock_inst0_out;
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
assign corebit_term_inst4_in = coreir_wrapInClock_inst0_out;
corebit_term corebit_term_inst4 (
    .in(corebit_term_inst4_in)
);
assign coreir_wrapInClock_inst0_in = CLK;
coreir_wrap coreir_wrapInClock_inst0 (
    .in(coreir_wrapInClock_inst0_in),
    .out(coreir_wrapInClock_inst0_out)
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

module Main (
    input CLK
);
wire RTL_inst0_CLK;
wire RTL_inst0_handshake_arr_0_ready;
wire RTL_inst0_handshake_arr_0_valid;
wire RTL_inst0_handshake_arr_1_ready;
wire RTL_inst0_handshake_arr_1_valid;
wire RTL_inst0_handshake_arr_2_ready;
wire RTL_inst0_handshake_arr_2_valid;
wire RTL_inst0_handshake_ready;
wire RTL_inst0_handshake_valid;
wire [3:0] RTL_inst0_in1;
wire [3:0] RTL_inst0_in2;
wire RTL_inst0_out;
wire RTL_inst1_CLK;
wire RTL_inst1_handshake_arr_0_ready;
wire RTL_inst1_handshake_arr_0_valid;
wire RTL_inst1_handshake_arr_1_ready;
wire RTL_inst1_handshake_arr_1_valid;
wire RTL_inst1_handshake_arr_2_ready;
wire RTL_inst1_handshake_arr_2_valid;
wire RTL_inst1_handshake_ready;
wire RTL_inst1_handshake_valid;
wire [4:0] RTL_inst1_in1;
wire [4:0] RTL_inst1_in2;
wire RTL_inst1_out;
wire corebit_term_inst0_in;
wire corebit_term_inst1_in;
wire corebit_term_inst10_in;
wire corebit_term_inst2_in;
wire corebit_term_inst3_in;
wire corebit_term_inst4_in;
wire corebit_term_inst5_in;
wire corebit_term_inst6_in;
wire corebit_term_inst7_in;
wire corebit_term_inst8_in;
wire corebit_term_inst9_in;
wire corebit_undriven_inst0_out;
wire corebit_undriven_inst1_out;
wire corebit_undriven_inst2_out;
wire corebit_undriven_inst3_out;
wire corebit_undriven_inst4_out;
wire corebit_undriven_inst5_out;
wire corebit_undriven_inst6_out;
wire corebit_undriven_inst7_out;
wire corebit_undriven_inst8_out;
wire corebit_undriven_inst9_out;
wire coreir_wrapInClock_inst0_in;
wire coreir_wrapInClock_inst0_out;
wire coreir_wrapOutClock_inst0_in;
wire coreir_wrapOutClock_inst0_out;
wire coreir_wrapOutClock_inst1_in;
wire coreir_wrapOutClock_inst1_out;
wire [3:0] undriven_inst0_out;
wire [3:0] undriven_inst1_out;
wire [4:0] undriven_inst2_out;
wire [4:0] undriven_inst3_out;
assign RTL_inst0_CLK = coreir_wrapOutClock_inst0_out;
assign RTL_inst0_handshake_arr_0_ready = corebit_undriven_inst2_out;
assign RTL_inst0_handshake_arr_1_ready = corebit_undriven_inst3_out;
assign RTL_inst0_handshake_arr_2_ready = corebit_undriven_inst4_out;
assign RTL_inst0_handshake_ready = corebit_undriven_inst1_out;
assign RTL_inst0_in1 = undriven_inst0_out;
assign RTL_inst0_in2 = undriven_inst1_out;
RTL RTL_inst0 (
    .CLK(RTL_inst0_CLK),
    .handshake_arr_0_ready(RTL_inst0_handshake_arr_0_ready),
    .handshake_arr_0_valid(RTL_inst0_handshake_arr_0_valid),
    .handshake_arr_1_ready(RTL_inst0_handshake_arr_1_ready),
    .handshake_arr_1_valid(RTL_inst0_handshake_arr_1_valid),
    .handshake_arr_2_ready(RTL_inst0_handshake_arr_2_ready),
    .handshake_arr_2_valid(RTL_inst0_handshake_arr_2_valid),
    .handshake_ready(RTL_inst0_handshake_ready),
    .handshake_valid(RTL_inst0_handshake_valid),
    .in1(RTL_inst0_in1),
    .in2(RTL_inst0_in2),
    .out(RTL_inst0_out)
);
assign RTL_inst1_CLK = coreir_wrapOutClock_inst1_out;
assign RTL_inst1_handshake_arr_0_ready = corebit_undriven_inst7_out;
assign RTL_inst1_handshake_arr_1_ready = corebit_undriven_inst8_out;
assign RTL_inst1_handshake_arr_2_ready = corebit_undriven_inst9_out;
assign RTL_inst1_handshake_ready = corebit_undriven_inst6_out;
assign RTL_inst1_in1 = undriven_inst2_out;
assign RTL_inst1_in2 = undriven_inst3_out;
RTL_unq1 RTL_inst1 (
    .CLK(RTL_inst1_CLK),
    .handshake_arr_0_ready(RTL_inst1_handshake_arr_0_ready),
    .handshake_arr_0_valid(RTL_inst1_handshake_arr_0_valid),
    .handshake_arr_1_ready(RTL_inst1_handshake_arr_1_ready),
    .handshake_arr_1_valid(RTL_inst1_handshake_arr_1_valid),
    .handshake_arr_2_ready(RTL_inst1_handshake_arr_2_ready),
    .handshake_arr_2_valid(RTL_inst1_handshake_arr_2_valid),
    .handshake_ready(RTL_inst1_handshake_ready),
    .handshake_valid(RTL_inst1_handshake_valid),
    .in1(RTL_inst1_in1),
    .in2(RTL_inst1_in2),
    .out(RTL_inst1_out)
);
assign corebit_term_inst0_in = coreir_wrapInClock_inst0_out;
corebit_term corebit_term_inst0 (
    .in(corebit_term_inst0_in)
);
assign corebit_term_inst1_in = RTL_inst0_out;
corebit_term corebit_term_inst1 (
    .in(corebit_term_inst1_in)
);
assign corebit_term_inst10_in = RTL_inst1_handshake_arr_2_valid;
corebit_term corebit_term_inst10 (
    .in(corebit_term_inst10_in)
);
assign corebit_term_inst2_in = RTL_inst0_handshake_valid;
corebit_term corebit_term_inst2 (
    .in(corebit_term_inst2_in)
);
assign corebit_term_inst3_in = RTL_inst0_handshake_arr_0_valid;
corebit_term corebit_term_inst3 (
    .in(corebit_term_inst3_in)
);
assign corebit_term_inst4_in = RTL_inst0_handshake_arr_1_valid;
corebit_term corebit_term_inst4 (
    .in(corebit_term_inst4_in)
);
assign corebit_term_inst5_in = RTL_inst0_handshake_arr_2_valid;
corebit_term corebit_term_inst5 (
    .in(corebit_term_inst5_in)
);
assign corebit_term_inst6_in = RTL_inst1_out;
corebit_term corebit_term_inst6 (
    .in(corebit_term_inst6_in)
);
assign corebit_term_inst7_in = RTL_inst1_handshake_valid;
corebit_term corebit_term_inst7 (
    .in(corebit_term_inst7_in)
);
assign corebit_term_inst8_in = RTL_inst1_handshake_arr_0_valid;
corebit_term corebit_term_inst8 (
    .in(corebit_term_inst8_in)
);
assign corebit_term_inst9_in = RTL_inst1_handshake_arr_1_valid;
corebit_term corebit_term_inst9 (
    .in(corebit_term_inst9_in)
);
corebit_undriven corebit_undriven_inst0 (
    .out(corebit_undriven_inst0_out)
);
corebit_undriven corebit_undriven_inst1 (
    .out(corebit_undriven_inst1_out)
);
corebit_undriven corebit_undriven_inst2 (
    .out(corebit_undriven_inst2_out)
);
corebit_undriven corebit_undriven_inst3 (
    .out(corebit_undriven_inst3_out)
);
corebit_undriven corebit_undriven_inst4 (
    .out(corebit_undriven_inst4_out)
);
corebit_undriven corebit_undriven_inst5 (
    .out(corebit_undriven_inst5_out)
);
corebit_undriven corebit_undriven_inst6 (
    .out(corebit_undriven_inst6_out)
);
corebit_undriven corebit_undriven_inst7 (
    .out(corebit_undriven_inst7_out)
);
corebit_undriven corebit_undriven_inst8 (
    .out(corebit_undriven_inst8_out)
);
corebit_undriven corebit_undriven_inst9 (
    .out(corebit_undriven_inst9_out)
);
assign coreir_wrapInClock_inst0_in = CLK;
coreir_wrap coreir_wrapInClock_inst0 (
    .in(coreir_wrapInClock_inst0_in),
    .out(coreir_wrapInClock_inst0_out)
);
assign coreir_wrapOutClock_inst0_in = corebit_undriven_inst0_out;
coreir_wrap coreir_wrapOutClock_inst0 (
    .in(coreir_wrapOutClock_inst0_in),
    .out(coreir_wrapOutClock_inst0_out)
);
assign coreir_wrapOutClock_inst1_in = corebit_undriven_inst5_out;
coreir_wrap coreir_wrapOutClock_inst1 (
    .in(coreir_wrapOutClock_inst1_in),
    .out(coreir_wrapOutClock_inst1_out)
);
coreir_undriven #(
    .width(4)
) undriven_inst0 (
    .out(undriven_inst0_out)
);
coreir_undriven #(
    .width(4)
) undriven_inst1 (
    .out(undriven_inst1_out)
);
coreir_undriven #(
    .width(5)
) undriven_inst2 (
    .out(undriven_inst2_out)
);
coreir_undriven #(
    .width(5)
) undriven_inst3 (
    .out(undriven_inst3_out)
);
endmodule

