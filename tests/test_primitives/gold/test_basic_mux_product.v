module Mux2xTupleX_Bits2_Y_Bits4 (
    input [1:0] I0_X,
    input [3:0] I0_Y,
    input [1:0] I1_X,
    input [3:0] I1_Y,
    output [1:0] O_X,
    output [3:0] O_Y,
    input S
);
reg [5:0] coreir_commonlib_mux2x6_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x6_inst0_out = {I0_Y,I0_X};
end else begin
    coreir_commonlib_mux2x6_inst0_out = {I1_Y,I1_X};
end
end

assign O_X = {coreir_commonlib_mux2x6_inst0_out[1],coreir_commonlib_mux2x6_inst0_out[0]};
assign O_Y = {coreir_commonlib_mux2x6_inst0_out[5],coreir_commonlib_mux2x6_inst0_out[4],coreir_commonlib_mux2x6_inst0_out[3],coreir_commonlib_mux2x6_inst0_out[2]};
endmodule

module test_basic_mux_product (
    input [1:0] I_0_X,
    input [3:0] I_0_Y,
    input [1:0] I_1_X,
    input [3:0] I_1_Y,
    output [1:0] O_X,
    output [3:0] O_Y,
    input S
);
Mux2xTupleX_Bits2_Y_Bits4 Mux2xTupleX_Bits2_Y_Bits4_inst0 (
    .I0_X(I_0_X),
    .I0_Y(I_0_Y),
    .I1_X(I_1_X),
    .I1_Y(I_1_Y),
    .O_X(O_X),
    .O_Y(O_Y),
    .S(S)
);
endmodule

