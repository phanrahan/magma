// Module `srem` defined externally
module TestBinary (
    input [2:0] I0,
    input [2:0] I1,
    output [2:0] O
);
wire [2:0] magma_Bits_3_srem_inst0_out;
coreir_srem__width3 magma_Bits_3_srem_inst0 (
    .in0(I0),
    .in1(I1),
    .out(magma_Bits_3_srem_inst0_out)
);
assign O = magma_Bits_3_srem_inst0_out;
endmodule

