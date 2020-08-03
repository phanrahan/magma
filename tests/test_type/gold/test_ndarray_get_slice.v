module Mux4xArray2_Array3_Array2_OutBit (
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
    coreir_commonlib_mux4x12_inst0_out = {I0[1][2][1:0],I0[1][1][1:0],I0[1][0][1:0],I0[0][2][1:0],I0[0][1][1:0],I0[0][0][1:0]};
end else if (S == 1) begin
    coreir_commonlib_mux4x12_inst0_out = {I1[1][2][1:0],I1[1][1][1:0],I1[1][0][1:0],I1[0][2][1:0],I1[0][1][1:0],I1[0][0][1:0]};
end else if (S == 2) begin
    coreir_commonlib_mux4x12_inst0_out = {I2[1][2][1:0],I2[1][1][1:0],I2[1][0][1:0],I2[0][2][1:0],I2[0][1][1:0],I2[0][0][1:0]};
end else begin
    coreir_commonlib_mux4x12_inst0_out = {I3[1][2][1:0],I3[1][1][1:0],I3[1][0][1:0],I3[0][2][1:0],I3[0][1][1:0],I3[0][0][1:0]};
end
end

assign O = '{'{coreir_commonlib_mux4x12_inst0_out[11:10],coreir_commonlib_mux4x12_inst0_out[9:8],coreir_commonlib_mux4x12_inst0_out[7:6]},'{coreir_commonlib_mux4x12_inst0_out[5:4],coreir_commonlib_mux4x12_inst0_out[3:2],coreir_commonlib_mux4x12_inst0_out[1:0]}};
endmodule

module Main (
    input [1:0] I [5:0][2:0],
    input [1:0] x,
    output [1:0] O [1:0][2:0]
);
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_I0 [1:0][2:0];
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_I1 [1:0][2:0];
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_I2 [1:0][2:0];
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_I3 [1:0][2:0];
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_S;
wire [1:0] Mux4xArray2_Array3_Array2_OutBit_inst0_O [1:0][2:0];
assign Mux4xArray2_Array3_Array2_OutBit_inst0_I0 = '{'{I[1][2],I[1][1],I[1][0]},'{I[0][2],I[0][1],I[0][0]}};
assign Mux4xArray2_Array3_Array2_OutBit_inst0_I1 = '{'{I[2][2],I[2][1],I[2][0]},'{I[1][2],I[1][1],I[1][0]}};
assign Mux4xArray2_Array3_Array2_OutBit_inst0_I2 = '{'{I[3][2],I[3][1],I[3][0]},'{I[2][2],I[2][1],I[2][0]}};
assign Mux4xArray2_Array3_Array2_OutBit_inst0_I3 = '{'{I[4][2],I[4][1],I[4][0]},'{I[3][2],I[3][1],I[3][0]}};
assign Mux4xArray2_Array3_Array2_OutBit_inst0_S = x;
Mux4xArray2_Array3_Array2_OutBit Mux4xArray2_Array3_Array2_OutBit_inst0 (
    .I0(Mux4xArray2_Array3_Array2_OutBit_inst0_I0),
    .I1(Mux4xArray2_Array3_Array2_OutBit_inst0_I1),
    .I2(Mux4xArray2_Array3_Array2_OutBit_inst0_I2),
    .I3(Mux4xArray2_Array3_Array2_OutBit_inst0_I3),
    .S(Mux4xArray2_Array3_Array2_OutBit_inst0_S),
    .O(Mux4xArray2_Array3_Array2_OutBit_inst0_O)
);
assign O = '{'{Mux4xArray2_Array3_Array2_OutBit_inst0_O[1][2],Mux4xArray2_Array3_Array2_OutBit_inst0_O[1][1],Mux4xArray2_Array3_Array2_OutBit_inst0_O[1][0]},'{Mux4xArray2_Array3_Array2_OutBit_inst0_O[0][2],Mux4xArray2_Array3_Array2_OutBit_inst0_O[0][1],Mux4xArray2_Array3_Array2_OutBit_inst0_O[0][0]}};
endmodule

