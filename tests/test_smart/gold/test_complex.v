module _Test (
    input [6:0] I0,
    input [8:0] I1,
    input [11:0] I2,
    output [9:0] O,
    output [6:0] O2,
    output [0:0] O3
);
wire magma_SInt_12_sle_inst0_out;
wire [11:0] magma_UInt_12_shl_inst0_out;
assign magma_SInt_12_sle_inst0_out = ($signed({I1[8],I1[8],I1[8],I1})) <= ($signed(I2));
assign magma_UInt_12_shl_inst0_out = (12'((~ (12'(({1'b0,1'b0,1'b0,1'b0,1'b0,I0}) + ({1'b0,1'b0,1'b0,I1})))) + I2)) << ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,& I0});
assign O = {magma_UInt_12_shl_inst0_out[9],magma_UInt_12_shl_inst0_out[8],magma_UInt_12_shl_inst0_out[7],magma_UInt_12_shl_inst0_out[6],magma_UInt_12_shl_inst0_out[5],magma_UInt_12_shl_inst0_out[4],magma_UInt_12_shl_inst0_out[3],magma_UInt_12_shl_inst0_out[2],magma_UInt_12_shl_inst0_out[1],magma_UInt_12_shl_inst0_out[0]};
assign O2 = 7'(({magma_SInt_12_sle_inst0_out,magma_SInt_12_sle_inst0_out,magma_SInt_12_sle_inst0_out,magma_SInt_12_sle_inst0_out,magma_SInt_12_sle_inst0_out,magma_SInt_12_sle_inst0_out,magma_SInt_12_sle_inst0_out}) + I0);
assign O3 = I0[0];
endmodule

