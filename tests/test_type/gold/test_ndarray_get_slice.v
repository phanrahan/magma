module Mux4xArray2_Array3_Array2_Bit (
    input [1:0] I0 [1:0][2:0],
    input [1:0] I1 [1:0][2:0],
    input [1:0] I2 [1:0][2:0],
    input [1:0] I3 [1:0][2:0],
    input [1:0] S,
    output [1:0] O [1:0][2:0]
);
reg [11:0] coreir_commonlib_mux4x12_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux4x12_inst0_out = {I0[1][2],I0[1][1],I0[1][0],I0[0][2],I0[0][1],I0[0][0]};
end else if (S == 1) begin
    coreir_commonlib_mux4x12_inst0_out = {I1[1][2],I1[1][1],I1[1][0],I1[0][2],I1[0][1],I1[0][0]};
end else if (S == 2) begin
    coreir_commonlib_mux4x12_inst0_out = {I2[1][2],I2[1][1],I2[1][0],I2[0][2],I2[0][1],I2[0][0]};
end else begin
    coreir_commonlib_mux4x12_inst0_out = {I3[1][2],I3[1][1],I3[1][0],I3[0][2],I3[0][1],I3[0][0]};
end
end

assign O[1][2] = {coreir_commonlib_mux4x12_inst0_out[11],coreir_commonlib_mux4x12_inst0_out[10]};
assign O[1][1] = {coreir_commonlib_mux4x12_inst0_out[9],coreir_commonlib_mux4x12_inst0_out[8]};
assign O[1][0] = {coreir_commonlib_mux4x12_inst0_out[7],coreir_commonlib_mux4x12_inst0_out[6]};
assign O[0][2] = {coreir_commonlib_mux4x12_inst0_out[5],coreir_commonlib_mux4x12_inst0_out[4]};
assign O[0][1] = {coreir_commonlib_mux4x12_inst0_out[3],coreir_commonlib_mux4x12_inst0_out[2]};
assign O[0][0] = {coreir_commonlib_mux4x12_inst0_out[1],coreir_commonlib_mux4x12_inst0_out[0]};
endmodule

module Main (
    input [1:0] I [5:0][2:0],
    input [1:0] x,
    output [1:0] O [1:0][2:0]
);
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst0_O [1:0][2:0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst0_I0 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[1][2] = I[1][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[1][1] = I[1][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[1][0] = I[1][0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[0][2] = I[0][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[0][1] = I[0][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I0[0][0] = I[0][0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst0_I1 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[1][2] = I[2][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[1][1] = I[2][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[1][0] = I[2][0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[0][2] = I[1][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[0][1] = I[1][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I1[0][0] = I[1][0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst0_I2 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[1][2] = I[3][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[1][1] = I[3][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[1][0] = I[3][0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[0][2] = I[2][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[0][1] = I[2][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I2[0][0] = I[2][0];
wire [1:0] Mux4xArray2_Array3_Array2_Bit_inst0_I3 [1:0][2:0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[1][2] = I[4][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[1][1] = I[4][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[1][0] = I[4][0];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[0][2] = I[3][2];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[0][1] = I[3][1];
assign Mux4xArray2_Array3_Array2_Bit_inst0_I3[0][0] = I[3][0];
Mux4xArray2_Array3_Array2_Bit Mux4xArray2_Array3_Array2_Bit_inst0 (
    .I0(Mux4xArray2_Array3_Array2_Bit_inst0_I0),
    .I1(Mux4xArray2_Array3_Array2_Bit_inst0_I1),
    .I2(Mux4xArray2_Array3_Array2_Bit_inst0_I2),
    .I3(Mux4xArray2_Array3_Array2_Bit_inst0_I3),
    .S(x),
    .O(Mux4xArray2_Array3_Array2_Bit_inst0_O)
);
assign O[1][2] = Mux4xArray2_Array3_Array2_Bit_inst0_O[1][2];
assign O[1][1] = Mux4xArray2_Array3_Array2_Bit_inst0_O[1][1];
assign O[1][0] = Mux4xArray2_Array3_Array2_Bit_inst0_O[1][0];
assign O[0][2] = Mux4xArray2_Array3_Array2_Bit_inst0_O[0][2];
assign O[0][1] = Mux4xArray2_Array3_Array2_Bit_inst0_O[0][1];
assign O[0][0] = Mux4xArray2_Array3_Array2_Bit_inst0_O[0][0];
endmodule

