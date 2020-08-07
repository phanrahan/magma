// Module `urem` defined externally
module TestBinary (
    input [2:0] I0,
    input [2:0] I1,
    output [2:0] O
);
wire [2:0] magma_Bits_3_urem_inst0_in0;
wire [2:0] magma_Bits_3_urem_inst0_in1;
wire [2:0] magma_Bits_3_urem_inst0_out;
assign magma_Bits_3_urem_inst0_in0 = I0;
assign magma_Bits_3_urem_inst0_in1 = I1;
coreir_urem__width3 magma_Bits_3_urem_inst0 (
    .in0(magma_Bits_3_urem_inst0_in0),
    .in1(magma_Bits_3_urem_inst0_in1),
    .out(magma_Bits_3_urem_inst0_out)
);
assign O = magma_Bits_3_urem_inst0_out;
endmodule

