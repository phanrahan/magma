module coreir_ule #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 <= in1;
endmodule

module TestBinary (
    input [0:0] I0,
    input [0:0] I1,
    output O
);
wire [0:0] magma_Bits_1_ule_inst0_in0;
wire [0:0] magma_Bits_1_ule_inst0_in1;
wire magma_Bits_1_ule_inst0_out;
assign magma_Bits_1_ule_inst0_in0 = I0;
assign magma_Bits_1_ule_inst0_in1 = I1;
coreir_ule #(
    .width(1)
) magma_Bits_1_ule_inst0 (
    .in0(magma_Bits_1_ule_inst0_in0),
    .in1(magma_Bits_1_ule_inst0_in1),
    .out(magma_Bits_1_ule_inst0_out)
);
assign O = magma_Bits_1_ule_inst0_out;
endmodule

