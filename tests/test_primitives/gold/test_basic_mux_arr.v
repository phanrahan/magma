module Mux2xArray2_Bits2 (
    input [1:0] I0 [1:0],
    input [1:0] I1 [1:0],
    input S,
    output [1:0] O [1:0]
);
reg [3:0] coreir_commonlib_mux2x4_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x4_inst0_out = {I0[1],I0[0]};
end else begin
    coreir_commonlib_mux2x4_inst0_out = {I1[1],I1[0]};
end
end

assign O[1] = {coreir_commonlib_mux2x4_inst0_out[3],coreir_commonlib_mux2x4_inst0_out[2]};
assign O[0] = {coreir_commonlib_mux2x4_inst0_out[1],coreir_commonlib_mux2x4_inst0_out[0]};
endmodule

module test_basic_mux_arr (
    input [1:0] I [1:0][1:0],
    input S,
    output [1:0] O [1:0]
);
wire [1:0] Mux2xArray2_Bits2_inst0_O [1:0];
wire [1:0] Mux2xArray2_Bits2_inst0_I0 [1:0];
assign Mux2xArray2_Bits2_inst0_I0[1] = I[0][1];
assign Mux2xArray2_Bits2_inst0_I0[0] = I[0][0];
wire [1:0] Mux2xArray2_Bits2_inst0_I1 [1:0];
assign Mux2xArray2_Bits2_inst0_I1[1] = I[1][1];
assign Mux2xArray2_Bits2_inst0_I1[0] = I[1][0];
Mux2xArray2_Bits2 Mux2xArray2_Bits2_inst0 (
    .I0(Mux2xArray2_Bits2_inst0_I0),
    .I1(Mux2xArray2_Bits2_inst0_I1),
    .S(S),
    .O(Mux2xArray2_Bits2_inst0_O)
);
assign O[1] = Mux2xArray2_Bits2_inst0_O[1];
assign O[0] = Mux2xArray2_Bits2_inst0_O[0];
endmodule

