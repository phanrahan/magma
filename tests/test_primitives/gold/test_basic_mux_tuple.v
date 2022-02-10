module Mux2xTupleBit_Bits2 (
    input I0__0,
    input [1:0] I0__1,
    input I1__0,
    input [1:0] I1__1,
    output O__0,
    output [1:0] O__1,
    input S
);
reg [2:0] coreir_commonlib_mux2x3_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x3_inst0_out = {I0__1,I0__0};
end else begin
    coreir_commonlib_mux2x3_inst0_out = {I1__1,I1__0};
end
end

assign O__0 = coreir_commonlib_mux2x3_inst0_out[0];
assign O__1 = {coreir_commonlib_mux2x3_inst0_out[2],coreir_commonlib_mux2x3_inst0_out[1]};
endmodule

module test_basic_mux_tuple (
    input I_0__0,
    input [1:0] I_0__1,
    input I_1__0,
    input [1:0] I_1__1,
    output O__0,
    output [1:0] O__1,
    input S
);
Mux2xTupleBit_Bits2 Mux2xTupleBit_Bits2_inst0 (
    .I0__0(I_0__0),
    .I0__1(I_0__1),
    .I1__0(I_1__0),
    .I1__1(I_1__1),
    .O__0(O__0),
    .O__1(O__1),
    .S(S)
);
endmodule

