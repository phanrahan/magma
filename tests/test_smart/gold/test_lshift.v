module _Test (
    input [7:0] I0,
    input [3:0] I1,
    output [7:0] O1,
    output [15:0] O2
);
wire [7:0] magma_UInt_8_shl_inst1_out;
assign magma_UInt_8_shl_inst1_out = I0 << ({1'b0,1'b0,1'b0,1'b0,I1[3],I1[2],I1[1],I1[0]});
assign O1 = I0 << ({1'b0,1'b0,1'b0,1'b0,I1[3],I1[2],I1[1],I1[0]});
assign O2 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,magma_UInt_8_shl_inst1_out[7],magma_UInt_8_shl_inst1_out[6],magma_UInt_8_shl_inst1_out[5],magma_UInt_8_shl_inst1_out[4],magma_UInt_8_shl_inst1_out[3],magma_UInt_8_shl_inst1_out[2],magma_UInt_8_shl_inst1_out[1],magma_UInt_8_shl_inst1_out[0]};
endmodule

