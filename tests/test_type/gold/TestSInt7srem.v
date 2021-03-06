// Module `srem` defined externally
module TestBinary (
    input [6:0] I0,
    input [6:0] I1,
    output [6:0] O
);
wire [6:0] magma_Bits_7_srem_inst0_out;
coreir_srem__width7 magma_Bits_7_srem_inst0 (
    .in0(I0),
    .in1(I1),
    .out(magma_Bits_7_srem_inst0_out)
);
assign O = magma_Bits_7_srem_inst0_out;
endmodule

