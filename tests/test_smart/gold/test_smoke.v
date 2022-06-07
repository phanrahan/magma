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
assign magma_UInt_16_add_inst0_out = 16'(({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port9}) + port10);
assign magma_UInt_16_shl_inst0_out = ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port22}) << port23;
assign port0 = {port1[9],port1[8],port1[7],port1[6],port1[5],port1[4],port1[3],port1[2],port1[1],port1[0]};
assign port2 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port3};
assign port4 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port5[0]};
assign port6 = port7[0];
assign port8 = {magma_UInt_16_add_inst0_out[11],magma_UInt_16_add_inst0_out[10],magma_UInt_16_add_inst0_out[9],magma_UInt_16_add_inst0_out[8],magma_UInt_16_add_inst0_out[7],magma_UInt_16_add_inst0_out[6],magma_UInt_16_add_inst0_out[5],magma_UInt_16_add_inst0_out[4],magma_UInt_16_add_inst0_out[3],magma_UInt_16_add_inst0_out[2],magma_UInt_16_add_inst0_out[1],magma_UInt_16_add_inst0_out[0]};
assign port11 = magma_UInt_10_add_inst0_out[0];
assign port14 = ~ ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port15});
assign port16 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port17}) <= port18};
assign port19 = {1'b0,1'b0,1'b0,& port20};
assign port21 = {magma_UInt_16_shl_inst0_out[9],magma_UInt_16_shl_inst0_out[8],magma_UInt_16_shl_inst0_out[7],magma_UInt_16_shl_inst0_out[6],magma_UInt_16_shl_inst0_out[5],magma_UInt_16_shl_inst0_out[4],magma_UInt_16_shl_inst0_out[3],magma_UInt_16_shl_inst0_out[2],magma_UInt_16_shl_inst0_out[1],magma_UInt_16_shl_inst0_out[0]};
assign port24 = port26 << ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port25});
assign port27 = port28 << ({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,port29[0]});
assign port30 = magma_UInt_10_shl_inst1_out[0];
assign port33 = {1'b0,1'b0,1'b0,1'b0,1'b0,port36[0],port35,port34};
endmodule

