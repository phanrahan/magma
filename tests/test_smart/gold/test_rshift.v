module _Test (
    input [7:0] I0,
    input [3:0] I1,
    output [3:0] O1,
    output [7:0] O2,
    output [15:0] O3
);
wire [7:0] magma_UInt_8_lshr_inst0_out;
assign magma_UInt_8_lshr_inst0_out = I0 >> ({1'b0,1'b0,1'b0,1'b0,I1});
assign O1 = {magma_UInt_8_lshr_inst0_out[3],magma_UInt_8_lshr_inst0_out[2],magma_UInt_8_lshr_inst0_out[1],magma_UInt_8_lshr_inst0_out[0]};
assign O2 = I0 >> ({1'b0,1'b0,1'b0,1'b0,I1});
assign O3 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,I0 >> ({1'b0,1'b0,1'b0,1'b0,I1})};
endmodule

