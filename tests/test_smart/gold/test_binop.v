module _Test (
    input [7:0] I0,
    input [11:0] I1,
    output [7:0] O1,
    output [11:0] O2,
    output [15:0] O3
);
wire [11:0] magma_UInt_12_add_inst0_out;
assign magma_UInt_12_add_inst0_out = 12'(({1'b0,1'b0,1'b0,1'b0,I0[7],I0[6],I0[5],I0[4],I0[3],I0[2],I0[1],I0[0]}) + I1);
assign O1 = magma_UInt_12_add_inst0_out[7:0];
assign O2 = 12'(({1'b0,1'b0,1'b0,1'b0,I0[7],I0[6],I0[5],I0[4],I0[3],I0[2],I0[1],I0[0]}) + I1);
assign O3 = 16'(({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,I0[7],I0[6],I0[5],I0[4],I0[3],I0[2],I0[1],I0[0]}) + ({1'b0,1'b0,1'b0,1'b0,I1[11],I1[10],I1[9],I1[8],I1[7],I1[6],I1[5],I1[4],I1[3],I1[2],I1[1],I1[0]}));
endmodule

