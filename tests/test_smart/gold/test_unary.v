module _Test (
    input [7:0] I0,
    output [3:0] O1,
    output [15:0] O2
);
wire [7:0] magma_Bits_8_not_inst0_out;
assign magma_Bits_8_not_inst0_out = ~ I0;
assign O1 = magma_Bits_8_not_inst0_out[3:0];
assign O2 = ~ ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,I0[7:0]});
endmodule

