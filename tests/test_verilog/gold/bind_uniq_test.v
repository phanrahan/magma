// Module `bar_foo_OtherCircuit` defined externally
module bar_coreir_wrap (
    input in,
    output out
);
  assign out = in;
endmodule

module bar_coreir_undriven #(
    parameter width = 1
) (
    output [width-1:0] out
);

endmodule

module bar_coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module bar_foo_SomeCircuit_unq1 (
    input [4:0] I
);
bar_coreir_term #(
    .width(5)
) term_inst0 (
    .in(I)
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
bar_foo_OtherCircuit other_circ (
    .x_y(x_y)
);
bar_coreir_term #(
    .width(20)
) term_inst0 (
    .in(_magma_bind_wire_0_0)
);
endmodule

module bar_corebit_undriven (
    output out
);

endmodule

module orr_5 (input [4:0] I, output O);
assign O = |(I);
endmodule
module orr_4 (input [3:0] I, output O);
assign O = |(I);
endmodule
module andr_5 (input [4:0] I, output O);
assign O = &(I);
endmodule
module andr_4 (input [3:0] I, output O);
assign O = &(I);
endmodule
module bar_corebit_term (
    input in
);

endmodule

module logical_and (input I0, input I1, output O);
assign O = I0 && I1;
endmodule
module bar_foo_RTL_unq1 (
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
    input [1:0] ndarr [2:0],
    output out
);
wire _magma_bind_wire_0;
wire _magma_bind_wire_1;
wire _magma_bind_wire_2_0;
wire _magma_bind_wire_2_1;
wire [4:0] _magma_bind_wire_3;
wire _magma_bind_wire_4;
wire [2:0] _magma_bind_wire_5_0;
wire [2:0] _magma_bind_wire_5_1;
wire andr_5_inst0_O;
wire coreir_wrapInClock_inst0_out;
wire [2:0] intermediate_ndarr_0;
wire [2:0] intermediate_ndarr_1;
wire [4:0] magma_Bits_5_xor_inst0_out;
wire [19:0] nested_other_circ_x_y [0:0];
wire orr_5_inst0_O;
wire temp3;
bar_foo_SomeCircuit_unq1 SomeCircuit_inst0 (
    .I(magma_Bits_5_xor_inst0_out)
);
assign _magma_bind_wire_0 = orr_5_inst0_O;
assign _magma_bind_wire_1 = andr_5_inst0_O;
assign _magma_bind_wire_2_0 = orr_5_inst0_O;
assign _magma_bind_wire_2_1 = andr_5_inst0_O;
assign _magma_bind_wire_3 = magma_Bits_5_xor_inst0_out;
assign _magma_bind_wire_4 = temp3;
assign _magma_bind_wire_5_0 = intermediate_ndarr_0;
assign _magma_bind_wire_5_1 = intermediate_ndarr_1;
andr_5 andr_5_inst0 (
    .I(in1),
    .O(andr_5_inst0_O)
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
bar_corebit_term corebit_term_inst12 (
    .in(coreir_wrapInClock_inst0_out)
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
bar_coreir_wrap coreir_wrapInClock_inst0 (
    .in(CLK),
    .out(coreir_wrapInClock_inst0_out)
);
assign intermediate_ndarr_0 = {ndarr[2][0],ndarr[1][0],ndarr[0][0]};
assign intermediate_ndarr_1 = {ndarr[2][1],ndarr[1][1],ndarr[0][1]};
logical_and logical_and_inst0 (
    .I0(orr_5_inst0_O),
    .I1(andr_5_inst0_O),
    .O(out)
);
assign magma_Bits_5_xor_inst0_out = in1 ^ in2;
bar_foo_NestedOtherCircuit nested_other_circ (
    .x_y(nested_other_circ_x_y)
);
orr_5 orr_5_inst0 (
    .I(in1),
    .O(orr_5_inst0_O)
);
assign temp3 = andr_5_inst0_O;
wire [5:0] term_inst0_in;
assign term_inst0_in = {ndarr[2],ndarr[1],ndarr[0]};
bar_coreir_term #(
    .width(6)
) term_inst0 (
    .in(term_inst0_in)
);
bar_coreir_term #(
    .width(5)
) term_inst1 (
    .in(_magma_bind_wire_3)
);
bar_coreir_term #(
    .width(20)
) term_inst2 (
    .in(nested_other_circ_x_y[0])
);
assign handshake_arr_0_valid = handshake_arr_2_ready;
assign handshake_arr_1_valid = handshake_arr_1_ready;
assign handshake_arr_2_valid = handshake_arr_0_ready;
assign handshake_valid = handshake_ready;
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
wire coreir_wrapInClock_inst0_out;
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
bar_corebit_term corebit_term_inst12 (
    .in(coreir_wrapInClock_inst0_out)
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
bar_coreir_wrap coreir_wrapInClock_inst0 (
    .in(CLK),
    .out(coreir_wrapInClock_inst0_out)
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
bar_coreir_term #(
    .width(20)
) term_inst2 (
    .in(nested_other_circ_x_y[0])
);
assign handshake_arr_0_valid = handshake_arr_2_ready;
assign handshake_arr_1_valid = handshake_arr_1_ready;
assign handshake_arr_2_valid = handshake_arr_0_ready;
assign handshake_valid = handshake_ready;
endmodule

module bar_foo_Main (
    input CLK
);
wire RTL_inst0_handshake_arr_0_valid;
wire RTL_inst0_handshake_arr_1_valid;
wire RTL_inst0_handshake_arr_2_valid;
wire RTL_inst0_handshake_valid;
wire RTL_inst0_out;
wire RTL_inst1_handshake_arr_0_valid;
wire RTL_inst1_handshake_arr_1_valid;
wire RTL_inst1_handshake_arr_2_valid;
wire RTL_inst1_handshake_valid;
wire RTL_inst1_out;
wire corebit_undriven_inst0_out;
wire corebit_undriven_inst1_out;
wire corebit_undriven_inst10_out;
wire corebit_undriven_inst11_out;
wire corebit_undriven_inst12_out;
wire corebit_undriven_inst13_out;
wire corebit_undriven_inst14_out;
wire corebit_undriven_inst15_out;
wire corebit_undriven_inst16_out;
wire corebit_undriven_inst17_out;
wire corebit_undriven_inst18_out;
wire corebit_undriven_inst19_out;
wire corebit_undriven_inst2_out;
wire corebit_undriven_inst3_out;
wire corebit_undriven_inst4_out;
wire corebit_undriven_inst5_out;
wire corebit_undriven_inst6_out;
wire corebit_undriven_inst7_out;
wire corebit_undriven_inst8_out;
wire corebit_undriven_inst9_out;
wire [3:0] undriven_inst0_out;
wire [3:0] undriven_inst1_out;
wire [4:0] undriven_inst2_out;
wire [4:0] undriven_inst3_out;
wire [1:0] RTL_inst0_ndarr [2:0];
assign RTL_inst0_ndarr[2] = {corebit_undriven_inst9_out,corebit_undriven_inst8_out};
assign RTL_inst0_ndarr[1] = {corebit_undriven_inst7_out,corebit_undriven_inst6_out};
assign RTL_inst0_ndarr[0] = {corebit_undriven_inst5_out,corebit_undriven_inst4_out};
bar_foo_RTL RTL_inst0 (
    .CLK(CLK),
    .handshake_arr_0_ready(corebit_undriven_inst1_out),
    .handshake_arr_0_valid(RTL_inst0_handshake_arr_0_valid),
    .handshake_arr_1_ready(corebit_undriven_inst2_out),
    .handshake_arr_1_valid(RTL_inst0_handshake_arr_1_valid),
    .handshake_arr_2_ready(corebit_undriven_inst3_out),
    .handshake_arr_2_valid(RTL_inst0_handshake_arr_2_valid),
    .handshake_ready(corebit_undriven_inst0_out),
    .handshake_valid(RTL_inst0_handshake_valid),
    .in1(undriven_inst0_out),
    .in2(undriven_inst1_out),
    .ndarr(RTL_inst0_ndarr),
    .out(RTL_inst0_out)
);
wire [1:0] RTL_inst1_ndarr [2:0];
assign RTL_inst1_ndarr[2] = {corebit_undriven_inst19_out,corebit_undriven_inst18_out};
assign RTL_inst1_ndarr[1] = {corebit_undriven_inst17_out,corebit_undriven_inst16_out};
assign RTL_inst1_ndarr[0] = {corebit_undriven_inst15_out,corebit_undriven_inst14_out};
bar_foo_RTL_unq1 RTL_inst1 (
    .CLK(CLK),
    .handshake_arr_0_ready(corebit_undriven_inst11_out),
    .handshake_arr_0_valid(RTL_inst1_handshake_arr_0_valid),
    .handshake_arr_1_ready(corebit_undriven_inst12_out),
    .handshake_arr_1_valid(RTL_inst1_handshake_arr_1_valid),
    .handshake_arr_2_ready(corebit_undriven_inst13_out),
    .handshake_arr_2_valid(RTL_inst1_handshake_arr_2_valid),
    .handshake_ready(corebit_undriven_inst10_out),
    .handshake_valid(RTL_inst1_handshake_valid),
    .in1(undriven_inst2_out),
    .in2(undriven_inst3_out),
    .ndarr(RTL_inst1_ndarr),
    .out(RTL_inst1_out)
);
bar_corebit_term corebit_term_inst0 (
    .in(RTL_inst0_out)
);
bar_corebit_term corebit_term_inst1 (
    .in(RTL_inst0_handshake_valid)
);
bar_corebit_term corebit_term_inst2 (
    .in(RTL_inst0_handshake_arr_0_valid)
);
bar_corebit_term corebit_term_inst3 (
    .in(RTL_inst0_handshake_arr_1_valid)
);
bar_corebit_term corebit_term_inst4 (
    .in(RTL_inst0_handshake_arr_2_valid)
);
bar_corebit_term corebit_term_inst5 (
    .in(RTL_inst1_out)
);
bar_corebit_term corebit_term_inst6 (
    .in(RTL_inst1_handshake_valid)
);
bar_corebit_term corebit_term_inst7 (
    .in(RTL_inst1_handshake_arr_0_valid)
);
bar_corebit_term corebit_term_inst8 (
    .in(RTL_inst1_handshake_arr_1_valid)
);
bar_corebit_term corebit_term_inst9 (
    .in(RTL_inst1_handshake_arr_2_valid)
);
bar_corebit_undriven corebit_undriven_inst0 (
    .out(corebit_undriven_inst0_out)
);
bar_corebit_undriven corebit_undriven_inst1 (
    .out(corebit_undriven_inst1_out)
);
bar_corebit_undriven corebit_undriven_inst10 (
    .out(corebit_undriven_inst10_out)
);
bar_corebit_undriven corebit_undriven_inst11 (
    .out(corebit_undriven_inst11_out)
);
bar_corebit_undriven corebit_undriven_inst12 (
    .out(corebit_undriven_inst12_out)
);
bar_corebit_undriven corebit_undriven_inst13 (
    .out(corebit_undriven_inst13_out)
);
bar_corebit_undriven corebit_undriven_inst14 (
    .out(corebit_undriven_inst14_out)
);
bar_corebit_undriven corebit_undriven_inst15 (
    .out(corebit_undriven_inst15_out)
);
bar_corebit_undriven corebit_undriven_inst16 (
    .out(corebit_undriven_inst16_out)
);
bar_corebit_undriven corebit_undriven_inst17 (
    .out(corebit_undriven_inst17_out)
);
bar_corebit_undriven corebit_undriven_inst18 (
    .out(corebit_undriven_inst18_out)
);
bar_corebit_undriven corebit_undriven_inst19 (
    .out(corebit_undriven_inst19_out)
);
bar_corebit_undriven corebit_undriven_inst2 (
    .out(corebit_undriven_inst2_out)
);
bar_corebit_undriven corebit_undriven_inst3 (
    .out(corebit_undriven_inst3_out)
);
bar_corebit_undriven corebit_undriven_inst4 (
    .out(corebit_undriven_inst4_out)
);
bar_corebit_undriven corebit_undriven_inst5 (
    .out(corebit_undriven_inst5_out)
);
bar_corebit_undriven corebit_undriven_inst6 (
    .out(corebit_undriven_inst6_out)
);
bar_corebit_undriven corebit_undriven_inst7 (
    .out(corebit_undriven_inst7_out)
);
bar_corebit_undriven corebit_undriven_inst8 (
    .out(corebit_undriven_inst8_out)
);
bar_corebit_undriven corebit_undriven_inst9 (
    .out(corebit_undriven_inst9_out)
);
bar_coreir_undriven #(
    .width(4)
) undriven_inst0 (
    .out(undriven_inst0_out)
);
bar_coreir_undriven #(
    .width(4)
) undriven_inst1 (
    .out(undriven_inst1_out)
);
bar_coreir_undriven #(
    .width(5)
) undriven_inst2 (
    .out(undriven_inst2_out)
);
bar_coreir_undriven #(
    .width(5)
) undriven_inst3 (
    .out(undriven_inst3_out)
);
endmodule

