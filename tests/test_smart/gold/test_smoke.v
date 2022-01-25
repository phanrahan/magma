module Test (
    output [9:0] port0,
    input [15:0] port1,
    output [15:0] port2,
    input [9:0] port3,
    output [9:0] port4,
    input [0:0] port5,
    output [0:0] port6,
    input [9:0] port7,
    output [11:0] port8,
    input [9:0] port9,
    input [15:0] port10,
    output [0:0] port11,
    input [9:0] port12,
    input [0:0] port13,
    output [15:0] port14,
    input [9:0] port15,
    output [11:0] port16,
    input [9:0] port17,
    input [15:0] port18,
    output [3:0] port19,
    input [9:0] port20,
    output [9:0] port21,
    input [9:0] port22,
    input [15:0] port23,
    output [15:0] port24,
    input [9:0] port25,
    input [15:0] port26,
    output [9:0] port27,
    input [9:0] port28,
    input [0:0] port29,
    output [0:0] port30,
    input [9:0] port31,
    input [0:0] port32,
    output [31:0] port33,
    input [9:0] port34,
    input [15:0] port35,
    input [0:0] port36
);
wire [9:0] magma_UInt_10_add_inst0_out;
wire [9:0] magma_UInt_10_shl_inst1_out;
wire [15:0] magma_UInt_16_add_inst0_out;
wire [15:0] magma_UInt_16_shl_inst0_out;
assign magma_UInt_10_add_inst0_out = 10'(port12 + ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port13[0]}));
assign magma_UInt_10_shl_inst1_out = ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port32[0]}) << port31;
assign magma_UInt_16_add_inst0_out = 16'(({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port9[9],port9[8],port9[7],port9[6],port9[5],port9[4],port9[3],port9[2],port9[1],port9[0]}) + port10);
assign magma_UInt_16_shl_inst0_out = ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port22[9],port22[8],port22[7],port22[6],port22[5],port22[4],port22[3],port22[2],port22[1],port22[0]}) << port23;
assign port0 = {port1[9],port1[8],port1[7],port1[6],port1[5],port1[4],port1[3],port1[2],port1[1],port1[0]};
assign port2 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port3[9],port3[8],port3[7],port3[6],port3[5],port3[4],port3[3],port3[2],port3[1],port3[0]};
assign port4 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port5[0]};
assign port6 = port7[0];
assign port8 = magma_UInt_16_add_inst0_out[11:0];
assign port11 = magma_UInt_10_add_inst0_out[0:0];
assign port14 = ~ ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port15[9],port15[8],port15[7],port15[6],port15[5],port15[4],port15[3],port15[2],port15[1],port15[0]});
assign port16 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port17[9],port17[8],port17[7],port17[6],port17[5],port17[4],port17[3],port17[2],port17[1],port17[0]}) <= port18};
assign port19 = {1'b0,1'b0,1'b0,& port20};
assign port21 = magma_UInt_16_shl_inst0_out[9:0];
assign port24 = port26 << ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port25[9],port25[8],port25[7],port25[6],port25[5],port25[4],port25[3],port25[2],port25[1],port25[0]});
assign port27 = port28 << ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port29[0]});
assign port30 = magma_UInt_10_shl_inst1_out[0:0];
assign port33 = {1'b0,1'b0,1'b0,1'b0,1'b0,port36[0],port35[15],port35[14],port35[13],port35[12],port35[11],port35[10],port35[9],port35[8],port35[7],port35[6],port35[5],port35[4],port35[3],port35[2],port35[1],port35[0],port34[9],port34[8],port34[7],port34[6],port34[5],port34[4],port34[3],port34[2],port34[1],port34[0]};
endmodule

