// Module `urem` defined externally
module TestBinary (
    input [0:0] I0,
    input [0:0] I1,
    output [0:0] O
);
wire [0:0] magma_Bits_1_urem_inst0_out;
coreir_urem__width1 magma_Bits_1_urem_inst0 (
    .in0(I0),
    .in1(I1),
    .out(magma_Bits_1_urem_inst0_out)
);
assign O = magma_Bits_1_urem_inst0_out;
endmodule

