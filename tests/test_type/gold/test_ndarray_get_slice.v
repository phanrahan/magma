module Mux4xArray2_Array3_Array2_OutBit (
    input [1:0] I0_0_0,
    input [1:0] I0_0_1,
    input [1:0] I0_0_2,
    input [1:0] I0_1_0,
    input [1:0] I0_1_1,
    input [1:0] I0_1_2,
    input [1:0] I1_0_0,
    input [1:0] I1_0_1,
    input [1:0] I1_0_2,
    input [1:0] I1_1_0,
    input [1:0] I1_1_1,
    input [1:0] I1_1_2,
    input [1:0] I2_0_0,
    input [1:0] I2_0_1,
    input [1:0] I2_0_2,
    input [1:0] I2_1_0,
    input [1:0] I2_1_1,
    input [1:0] I2_1_2,
    input [1:0] I3_0_0,
    input [1:0] I3_0_1,
    input [1:0] I3_0_2,
    input [1:0] I3_1_0,
    input [1:0] I3_1_1,
    input [1:0] I3_1_2,
    output [1:0] O_0_0,
    output [1:0] O_0_1,
    output [1:0] O_0_2,
    output [1:0] O_1_0,
    output [1:0] O_1_1,
    output [1:0] O_1_2,
    input [1:0] S
);
reg [11:0] coreir_commonlib_mux4x12_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux4x12_inst0_out = {I0_1_2[1:0],I0_1_1[1:0],I0_1_0[1:0],I0_0_2[1:0],I0_0_1[1:0],I0_0_0[1:0]};
end else if (S == 1) begin
    coreir_commonlib_mux4x12_inst0_out = {I1_1_2[1:0],I1_1_1[1:0],I1_1_0[1:0],I1_0_2[1:0],I1_0_1[1:0],I1_0_0[1:0]};
end else if (S == 2) begin
    coreir_commonlib_mux4x12_inst0_out = {I2_1_2[1:0],I2_1_1[1:0],I2_1_0[1:0],I2_0_2[1:0],I2_0_1[1:0],I2_0_0[1:0]};
end else begin
    coreir_commonlib_mux4x12_inst0_out = {I3_1_2[1:0],I3_1_1[1:0],I3_1_0[1:0],I3_0_2[1:0],I3_0_1[1:0],I3_0_0[1:0]};
end
end

assign O_0_0 = coreir_commonlib_mux4x12_inst0_out[1:0];
assign O_0_1 = coreir_commonlib_mux4x12_inst0_out[3:2];
assign O_0_2 = coreir_commonlib_mux4x12_inst0_out[5:4];
assign O_1_0 = coreir_commonlib_mux4x12_inst0_out[7:6];
assign O_1_1 = coreir_commonlib_mux4x12_inst0_out[9:8];
assign O_1_2 = coreir_commonlib_mux4x12_inst0_out[11:10];
endmodule

module Main (
    input [1:0] I_0_0,
    input [1:0] I_0_1,
    input [1:0] I_0_2,
    input [1:0] I_1_0,
    input [1:0] I_1_1,
    input [1:0] I_1_2,
    input [1:0] I_2_0,
    input [1:0] I_2_1,
    input [1:0] I_2_2,
    input [1:0] I_3_0,
    input [1:0] I_3_1,
    input [1:0] I_3_2,
    input [1:0] I_4_0,
    input [1:0] I_4_1,
    input [1:0] I_4_2,
    input [1:0] I_5_0,
    input [1:0] I_5_1,
    input [1:0] I_5_2,
    output [1:0] O_0_0,
    output [1:0] O_0_1,
    output [1:0] O_0_2,
    output [1:0] O_1_0,
    output [1:0] O_1_1,
    output [1:0] O_1_2,
    input [1:0] x
);
Mux4xArray2_Array3_Array2_OutBit Mux4xArray2_Array3_Array2_OutBit_inst0 (
    .I0_0_0(I_0_0),
    .I0_0_1(I_0_1),
    .I0_0_2(I_0_2),
    .I0_1_0(I_1_0),
    .I0_1_1(I_1_1),
    .I0_1_2(I_1_2),
    .I1_0_0(I_1_0),
    .I1_0_1(I_1_1),
    .I1_0_2(I_1_2),
    .I1_1_0(I_2_0),
    .I1_1_1(I_2_1),
    .I1_1_2(I_2_2),
    .I2_0_0(I_2_0),
    .I2_0_1(I_2_1),
    .I2_0_2(I_2_2),
    .I2_1_0(I_3_0),
    .I2_1_1(I_3_1),
    .I2_1_2(I_3_2),
    .I3_0_0(I_3_0),
    .I3_0_1(I_3_1),
    .I3_0_2(I_3_2),
    .I3_1_0(I_4_0),
    .I3_1_1(I_4_1),
    .I3_1_2(I_4_2),
    .O_0_0(O_0_0),
    .O_0_1(O_0_1),
    .O_0_2(O_0_2),
    .O_1_0(O_1_0),
    .O_1_1(O_1_1),
    .O_1_2(O_1_2),
    .S(x)
);
endmodule

