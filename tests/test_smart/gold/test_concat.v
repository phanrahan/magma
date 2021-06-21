module _Test (
    input [7:0] I0,
    input [3:0] I1,
    input [9:0] I2,
    output [3:0] O1,
    output [15:0] O2
);
wire [7:0] magma_UInt_8_add_inst0_out;
wire [7:0] magma_UInt_8_add_inst1_out;
assign magma_UInt_8_add_inst0_out = 8'(I0 + ({1'b0,1'b0,1'b0,1'b0,I1[3:0]}));
assign magma_UInt_8_add_inst1_out = 8'(I0 + ({1'b0,1'b0,1'b0,1'b0,I1[3:0]}));
assign O1 = magma_UInt_8_add_inst0_out[3:0];
assign O2 = {I2[7:0],magma_UInt_8_add_inst1_out[7:0]};
endmodule

