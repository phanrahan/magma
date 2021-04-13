// Module `coreir_urem__width3` defined externally
module TestBinary (
    input [2:0] I0,
    input [2:0] I1,
    output [2:0] O
);
wire [2:0] magma_UInt_3_urem_inst0_out;
coreir_urem__width3 magma_UInt_3_urem_inst0 (
    .in0(I0),
    .in1(I1),
    .out(magma_UInt_3_urem_inst0_out)
);
assign O = magma_UInt_3_urem_inst0_out;
endmodule

