module Mux2xArray3_Array2_Bit (
    input [1:0] I0 [2:0],
    input [1:0] I1 [2:0],
    input S,
    output [1:0] O [2:0]
);
reg [5:0] coreir_commonlib_mux2x6_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x6_inst0_out = {I0[2],I0[1],I0[0]};
end else begin
    coreir_commonlib_mux2x6_inst0_out = {I1[2],I1[1],I1[0]};
end
end

assign O[2] = {coreir_commonlib_mux2x6_inst0_out[5],coreir_commonlib_mux2x6_inst0_out[4]};
assign O[1] = {coreir_commonlib_mux2x6_inst0_out[3],coreir_commonlib_mux2x6_inst0_out[2]};
assign O[0] = {coreir_commonlib_mux2x6_inst0_out[1],coreir_commonlib_mux2x6_inst0_out[0]};
endmodule

module Main (
    input [1:0] I [1:0][2:0],
    input [1:0] x,
    output [1:0] O [5:0][2:0]
);
wire [1:0] Mux2xArray3_Array2_Bit_inst0_O [2:0];
wire [1:0] Mux2xArray3_Array2_Bit_inst1_O [2:0];
wire [1:0] Mux2xArray3_Array2_Bit_inst10_O [2:0];
wire [1:0] Mux2xArray3_Array2_Bit_inst11_O [2:0];
wire [1:0] Mux2xArray3_Array2_Bit_inst2_O [2:0];
wire [1:0] Mux2xArray3_Array2_Bit_inst3_O [2:0];
wire [1:0] Mux2xArray3_Array2_Bit_inst4_O [2:0];
wire [1:0] Mux2xArray3_Array2_Bit_inst5_O [2:0];
wire [1:0] Mux2xArray3_Array2_Bit_inst6_O [2:0];
wire [1:0] Mux2xArray3_Array2_Bit_inst7_O [2:0];
wire [1:0] Mux2xArray3_Array2_Bit_inst8_O [2:0];
wire [1:0] Mux2xArray3_Array2_Bit_inst9_O [2:0];
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst4_out;
wire magma_Bit_and_inst5_out;
wire magma_Bit_and_inst6_out;
wire magma_Bit_and_inst7_out;
wire [2:0] magma_UInt_3_sub_inst0_out;
wire [2:0] magma_UInt_3_sub_inst10_out;
wire [2:0] magma_UInt_3_sub_inst2_out;
wire [2:0] magma_UInt_3_sub_inst4_out;
wire [2:0] magma_UInt_3_sub_inst6_out;
wire [2:0] magma_UInt_3_sub_inst8_out;
wire [1:0] Mux2xArray3_Array2_Bit_inst0_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst0_I0[2] = I[0][2];
assign Mux2xArray3_Array2_Bit_inst0_I0[1] = I[0][1];
assign Mux2xArray3_Array2_Bit_inst0_I0[0] = I[0][0];
wire [1:0] Mux2xArray3_Array2_Bit_inst0_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst0_I1[2] = I[1][2];
assign Mux2xArray3_Array2_Bit_inst0_I1[1] = I[1][1];
assign Mux2xArray3_Array2_Bit_inst0_I1[0] = I[1][0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst0 (
    .I0(Mux2xArray3_Array2_Bit_inst0_I0),
    .I1(Mux2xArray3_Array2_Bit_inst0_I1),
    .S(magma_UInt_3_sub_inst0_out[0]),
    .O(Mux2xArray3_Array2_Bit_inst0_O)
);
wire [1:0] Mux2xArray3_Array2_Bit_inst1_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst1_I0[2] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst1_I0[1] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst1_I0[0] = {1'b0,1'b0};
wire [1:0] Mux2xArray3_Array2_Bit_inst1_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst1_I1[2] = Mux2xArray3_Array2_Bit_inst0_O[2];
assign Mux2xArray3_Array2_Bit_inst1_I1[1] = Mux2xArray3_Array2_Bit_inst0_O[1];
assign Mux2xArray3_Array2_Bit_inst1_I1[0] = Mux2xArray3_Array2_Bit_inst0_O[0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst1 (
    .I0(Mux2xArray3_Array2_Bit_inst1_I0),
    .I1(Mux2xArray3_Array2_Bit_inst1_I1),
    .S(magma_Bit_and_inst0_out),
    .O(Mux2xArray3_Array2_Bit_inst1_O)
);
wire [1:0] Mux2xArray3_Array2_Bit_inst10_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst10_I0[2] = I[0][2];
assign Mux2xArray3_Array2_Bit_inst10_I0[1] = I[0][1];
assign Mux2xArray3_Array2_Bit_inst10_I0[0] = I[0][0];
wire [1:0] Mux2xArray3_Array2_Bit_inst10_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst10_I1[2] = I[1][2];
assign Mux2xArray3_Array2_Bit_inst10_I1[1] = I[1][1];
assign Mux2xArray3_Array2_Bit_inst10_I1[0] = I[1][0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst10 (
    .I0(Mux2xArray3_Array2_Bit_inst10_I0),
    .I1(Mux2xArray3_Array2_Bit_inst10_I1),
    .S(magma_UInt_3_sub_inst10_out[0]),
    .O(Mux2xArray3_Array2_Bit_inst10_O)
);
wire [1:0] Mux2xArray3_Array2_Bit_inst11_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst11_I0[2] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst11_I0[1] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst11_I0[0] = {1'b0,1'b0};
wire [1:0] Mux2xArray3_Array2_Bit_inst11_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst11_I1[2] = Mux2xArray3_Array2_Bit_inst10_O[2];
assign Mux2xArray3_Array2_Bit_inst11_I1[1] = Mux2xArray3_Array2_Bit_inst10_O[1];
assign Mux2xArray3_Array2_Bit_inst11_I1[0] = Mux2xArray3_Array2_Bit_inst10_O[0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst11 (
    .I0(Mux2xArray3_Array2_Bit_inst11_I0),
    .I1(Mux2xArray3_Array2_Bit_inst11_I1),
    .S(magma_Bit_and_inst7_out),
    .O(Mux2xArray3_Array2_Bit_inst11_O)
);
wire [1:0] Mux2xArray3_Array2_Bit_inst2_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst2_I0[2] = I[0][2];
assign Mux2xArray3_Array2_Bit_inst2_I0[1] = I[0][1];
assign Mux2xArray3_Array2_Bit_inst2_I0[0] = I[0][0];
wire [1:0] Mux2xArray3_Array2_Bit_inst2_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst2_I1[2] = I[1][2];
assign Mux2xArray3_Array2_Bit_inst2_I1[1] = I[1][1];
assign Mux2xArray3_Array2_Bit_inst2_I1[0] = I[1][0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst2 (
    .I0(Mux2xArray3_Array2_Bit_inst2_I0),
    .I1(Mux2xArray3_Array2_Bit_inst2_I1),
    .S(magma_UInt_3_sub_inst2_out[0]),
    .O(Mux2xArray3_Array2_Bit_inst2_O)
);
wire [1:0] Mux2xArray3_Array2_Bit_inst3_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst3_I0[2] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst3_I0[1] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst3_I0[0] = {1'b0,1'b0};
wire [1:0] Mux2xArray3_Array2_Bit_inst3_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst3_I1[2] = Mux2xArray3_Array2_Bit_inst2_O[2];
assign Mux2xArray3_Array2_Bit_inst3_I1[1] = Mux2xArray3_Array2_Bit_inst2_O[1];
assign Mux2xArray3_Array2_Bit_inst3_I1[0] = Mux2xArray3_Array2_Bit_inst2_O[0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst3 (
    .I0(Mux2xArray3_Array2_Bit_inst3_I0),
    .I1(Mux2xArray3_Array2_Bit_inst3_I1),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xArray3_Array2_Bit_inst3_O)
);
wire [1:0] Mux2xArray3_Array2_Bit_inst4_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst4_I0[2] = I[0][2];
assign Mux2xArray3_Array2_Bit_inst4_I0[1] = I[0][1];
assign Mux2xArray3_Array2_Bit_inst4_I0[0] = I[0][0];
wire [1:0] Mux2xArray3_Array2_Bit_inst4_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst4_I1[2] = I[1][2];
assign Mux2xArray3_Array2_Bit_inst4_I1[1] = I[1][1];
assign Mux2xArray3_Array2_Bit_inst4_I1[0] = I[1][0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst4 (
    .I0(Mux2xArray3_Array2_Bit_inst4_I0),
    .I1(Mux2xArray3_Array2_Bit_inst4_I1),
    .S(magma_UInt_3_sub_inst4_out[0]),
    .O(Mux2xArray3_Array2_Bit_inst4_O)
);
wire [1:0] Mux2xArray3_Array2_Bit_inst5_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst5_I0[2] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst5_I0[1] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst5_I0[0] = {1'b0,1'b0};
wire [1:0] Mux2xArray3_Array2_Bit_inst5_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst5_I1[2] = Mux2xArray3_Array2_Bit_inst4_O[2];
assign Mux2xArray3_Array2_Bit_inst5_I1[1] = Mux2xArray3_Array2_Bit_inst4_O[1];
assign Mux2xArray3_Array2_Bit_inst5_I1[0] = Mux2xArray3_Array2_Bit_inst4_O[0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst5 (
    .I0(Mux2xArray3_Array2_Bit_inst5_I0),
    .I1(Mux2xArray3_Array2_Bit_inst5_I1),
    .S(magma_Bit_and_inst4_out),
    .O(Mux2xArray3_Array2_Bit_inst5_O)
);
wire [1:0] Mux2xArray3_Array2_Bit_inst6_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst6_I0[2] = I[0][2];
assign Mux2xArray3_Array2_Bit_inst6_I0[1] = I[0][1];
assign Mux2xArray3_Array2_Bit_inst6_I0[0] = I[0][0];
wire [1:0] Mux2xArray3_Array2_Bit_inst6_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst6_I1[2] = I[1][2];
assign Mux2xArray3_Array2_Bit_inst6_I1[1] = I[1][1];
assign Mux2xArray3_Array2_Bit_inst6_I1[0] = I[1][0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst6 (
    .I0(Mux2xArray3_Array2_Bit_inst6_I0),
    .I1(Mux2xArray3_Array2_Bit_inst6_I1),
    .S(magma_UInt_3_sub_inst6_out[0]),
    .O(Mux2xArray3_Array2_Bit_inst6_O)
);
wire [1:0] Mux2xArray3_Array2_Bit_inst7_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst7_I0[2] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst7_I0[1] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst7_I0[0] = {1'b0,1'b0};
wire [1:0] Mux2xArray3_Array2_Bit_inst7_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst7_I1[2] = Mux2xArray3_Array2_Bit_inst6_O[2];
assign Mux2xArray3_Array2_Bit_inst7_I1[1] = Mux2xArray3_Array2_Bit_inst6_O[1];
assign Mux2xArray3_Array2_Bit_inst7_I1[0] = Mux2xArray3_Array2_Bit_inst6_O[0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst7 (
    .I0(Mux2xArray3_Array2_Bit_inst7_I0),
    .I1(Mux2xArray3_Array2_Bit_inst7_I1),
    .S(magma_Bit_and_inst5_out),
    .O(Mux2xArray3_Array2_Bit_inst7_O)
);
wire [1:0] Mux2xArray3_Array2_Bit_inst8_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst8_I0[2] = I[0][2];
assign Mux2xArray3_Array2_Bit_inst8_I0[1] = I[0][1];
assign Mux2xArray3_Array2_Bit_inst8_I0[0] = I[0][0];
wire [1:0] Mux2xArray3_Array2_Bit_inst8_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst8_I1[2] = I[1][2];
assign Mux2xArray3_Array2_Bit_inst8_I1[1] = I[1][1];
assign Mux2xArray3_Array2_Bit_inst8_I1[0] = I[1][0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst8 (
    .I0(Mux2xArray3_Array2_Bit_inst8_I0),
    .I1(Mux2xArray3_Array2_Bit_inst8_I1),
    .S(magma_UInt_3_sub_inst8_out[0]),
    .O(Mux2xArray3_Array2_Bit_inst8_O)
);
wire [1:0] Mux2xArray3_Array2_Bit_inst9_I0 [2:0];
assign Mux2xArray3_Array2_Bit_inst9_I0[2] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst9_I0[1] = {1'b0,1'b0};
assign Mux2xArray3_Array2_Bit_inst9_I0[0] = {1'b0,1'b0};
wire [1:0] Mux2xArray3_Array2_Bit_inst9_I1 [2:0];
assign Mux2xArray3_Array2_Bit_inst9_I1[2] = Mux2xArray3_Array2_Bit_inst8_O[2];
assign Mux2xArray3_Array2_Bit_inst9_I1[1] = Mux2xArray3_Array2_Bit_inst8_O[1];
assign Mux2xArray3_Array2_Bit_inst9_I1[0] = Mux2xArray3_Array2_Bit_inst8_O[0];
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst9 (
    .I0(Mux2xArray3_Array2_Bit_inst9_I0),
    .I1(Mux2xArray3_Array2_Bit_inst9_I1),
    .S(magma_Bit_and_inst6_out),
    .O(Mux2xArray3_Array2_Bit_inst9_O)
);
assign magma_Bit_and_inst0_out = 1'b1 & (({1'b0,x}) <= 3'h0);
assign magma_Bit_and_inst2_out = (1'b1 & (({1'b0,x}) <= 3'h1)) & ((3'((3'(({1'b0,x}) + 3'h2)) - 3'h1)) >= 3'h1);
assign magma_Bit_and_inst4_out = (1'b1 & (({1'b0,x}) <= 3'h2)) & ((3'((3'(({1'b0,x}) + 3'h2)) - 3'h1)) >= 3'h2);
assign magma_Bit_and_inst5_out = 1'b1 & ((3'((3'(({1'b0,x}) + 3'h2)) - 3'h1)) >= 3'h3);
assign magma_Bit_and_inst6_out = 1'b1 & ((3'((3'(({1'b0,x}) + 3'h2)) - 3'h1)) >= 3'h4);
assign magma_Bit_and_inst7_out = 1'b1 & ((3'((3'(({1'b0,x}) + 3'h2)) - 3'h1)) >= 3'h5);
assign magma_UInt_3_sub_inst0_out = 3'(3'h0 - ({1'b0,x}));
assign magma_UInt_3_sub_inst10_out = 3'(3'h5 - ({1'b0,x}));
assign magma_UInt_3_sub_inst2_out = 3'(3'h1 - ({1'b0,x}));
assign magma_UInt_3_sub_inst4_out = 3'(3'h2 - ({1'b0,x}));
assign magma_UInt_3_sub_inst6_out = 3'(3'h3 - ({1'b0,x}));
assign magma_UInt_3_sub_inst8_out = 3'(3'h4 - ({1'b0,x}));
assign O[5][2] = Mux2xArray3_Array2_Bit_inst11_O[2];
assign O[5][1] = Mux2xArray3_Array2_Bit_inst11_O[1];
assign O[5][0] = Mux2xArray3_Array2_Bit_inst11_O[0];
assign O[4][2] = Mux2xArray3_Array2_Bit_inst9_O[2];
assign O[4][1] = Mux2xArray3_Array2_Bit_inst9_O[1];
assign O[4][0] = Mux2xArray3_Array2_Bit_inst9_O[0];
assign O[3][2] = Mux2xArray3_Array2_Bit_inst7_O[2];
assign O[3][1] = Mux2xArray3_Array2_Bit_inst7_O[1];
assign O[3][0] = Mux2xArray3_Array2_Bit_inst7_O[0];
assign O[2][2] = Mux2xArray3_Array2_Bit_inst5_O[2];
assign O[2][1] = Mux2xArray3_Array2_Bit_inst5_O[1];
assign O[2][0] = Mux2xArray3_Array2_Bit_inst5_O[0];
assign O[1][2] = Mux2xArray3_Array2_Bit_inst3_O[2];
assign O[1][1] = Mux2xArray3_Array2_Bit_inst3_O[1];
assign O[1][0] = Mux2xArray3_Array2_Bit_inst3_O[0];
assign O[0][2] = Mux2xArray3_Array2_Bit_inst1_O[2];
assign O[0][1] = Mux2xArray3_Array2_Bit_inst1_O[1];
assign O[0][0] = Mux2xArray3_Array2_Bit_inst1_O[0];
endmodule

