module _Test (
    input [7:0] I0,
    input [11:0] I1,
    output [7:0] O1,
    output [11:0] O2,
    output [15:0] O3
);
wire [11:0] magma_UInt_12_add_inst0_out;
assign magma_UInt_12_add_inst0_out = 12'(({1'b0,1'b0,1'b0,1'b0,I0[7:0]}) + I1);
assign O1 = magma_UInt_12_add_inst0_out[7:0];
assign O2 = 12'(({1'b0,1'b0,1'b0,1'b0,I0[7:0]}) + I1);
assign O3 = 16'(({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,I0[7:0]}) + ({1'b0,1'b0,1'b0,1'b0,I1[11:0]}));
endmodule

