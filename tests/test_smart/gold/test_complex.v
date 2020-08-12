module _Test (
    input [6:0] I0,
    input [8:0] I1,
    input [11:0] I2,
    output [9:0] O,
    output [6:0] O2,
    output [0:0] O3
);
wire [11:0] magma_Bits_12_shl_inst0_out;
wire magma_Bits_12_sle_inst0_out;
assign magma_Bits_12_shl_inst0_out = (12'((~ (12'(({1'b0,1'b0,1'b0,1'b0,1'b0,I0[6:0]}) + ({I1[8],I1[8],I1[8],I1[8:0]})))) + I2)) << ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,& I0});
assign magma_Bits_12_sle_inst0_out = ($signed({I1[8],I1[8],I1[8],I1[8:0]})) <= ($signed(I2));
assign O = magma_Bits_12_shl_inst0_out[9:0];
assign O2 = 7'(({magma_Bits_12_sle_inst0_out,magma_Bits_12_sle_inst0_out,magma_Bits_12_sle_inst0_out,magma_Bits_12_sle_inst0_out,magma_Bits_12_sle_inst0_out,magma_Bits_12_sle_inst0_out,magma_Bits_12_sle_inst0_out}) + I0);
assign O3 = I0[0];
endmodule

