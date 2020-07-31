module Mux2xArray3_Array2_OutBit (
    input [1:0][2:0] I0,
    input [1:0][2:0] I1,
    input S,
    output [1:0][2:0] O
);
reg [5:0] coreir_commonlib_mux2x6_inst0_out;
reg [5:0][1:0] coreir_commonlib_mux2x6_inst0_in_data;
always @(*) begin
coreir_commonlib_mux2x6_inst0_in_data = {{I1[2][1:0],I1[1][1:0],I1[0][1:0]},{I0[2][1:0],I0[1][1:0],I0[0][1:0]}};
if (S == 0) begin
    coreir_commonlib_mux2x6_inst0_out = coreir_commonlib_mux2x6_inst0_in_data[0];
end else begin
    coreir_commonlib_mux2x6_inst0_out = coreir_commonlib_mux2x6_inst0_in_data[1];
end
end

assign O = {coreir_commonlib_mux2x6_inst0_out[5:4],{coreir_commonlib_mux2x6_inst0_out[3:2],coreir_commonlib_mux2x6_inst0_out[1:0]}};
endmodule

module Main (
    input [1:0][2:0][1:0] I,
    input [1:0] x,
    output [1:0][2:0][5:0] O
);
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst0_O;
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst1_O;
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst10_O;
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst11_O;
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst2_O;
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst3_O;
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst4_O;
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst5_O;
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst6_O;
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst7_O;
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst8_O;
wire [1:0][2:0] Mux2xArray3_Array2_OutBit_inst9_O;
wire [2:0] magma_Bits_3_sub_inst0_out;
wire [2:0] magma_Bits_3_sub_inst10_out;
wire [2:0] magma_Bits_3_sub_inst2_out;
wire [2:0] magma_Bits_3_sub_inst4_out;
wire [2:0] magma_Bits_3_sub_inst6_out;
wire [2:0] magma_Bits_3_sub_inst8_out;
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst0 (
    .I0({I[0][2],{I[0][1],I[0][0]}}),
    .I1({I[1][2],{I[1][1],I[1][0]}}),
    .S(magma_Bits_3_sub_inst0_out[0]),
    .O(Mux2xArray3_Array2_OutBit_inst0_O)
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst1 (
    .I0({{1'b0,1'b0,1'b0},{1'b0,1'b0,1'b0}}),
    .I1({Mux2xArray3_Array2_OutBit_inst0_O[2],{Mux2xArray3_Array2_OutBit_inst0_O[1],Mux2xArray3_Array2_OutBit_inst0_O[0]}}),
    .S(1'b1 & (({1'b0,x[1:0]}) <= 3'h0)),
    .O(Mux2xArray3_Array2_OutBit_inst1_O)
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst10 (
    .I0({I[0][2],{I[0][1],I[0][0]}}),
    .I1({I[1][2],{I[1][1],I[1][0]}}),
    .S(magma_Bits_3_sub_inst10_out[0]),
    .O(Mux2xArray3_Array2_OutBit_inst10_O)
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst11 (
    .I0({{1'b0,1'b0,1'b0},{1'b0,1'b0,1'b0}}),
    .I1({Mux2xArray3_Array2_OutBit_inst10_O[2],{Mux2xArray3_Array2_OutBit_inst10_O[1],Mux2xArray3_Array2_OutBit_inst10_O[0]}}),
    .S(1'b1 & ((3'((3'(({1'b0,x[1:0]}) + 3'h2)) - 3'h1)) >= 3'h5)),
    .O(Mux2xArray3_Array2_OutBit_inst11_O)
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst2 (
    .I0({I[0][2],{I[0][1],I[0][0]}}),
    .I1({I[1][2],{I[1][1],I[1][0]}}),
    .S(magma_Bits_3_sub_inst2_out[0]),
    .O(Mux2xArray3_Array2_OutBit_inst2_O)
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst3 (
    .I0({{1'b0,1'b0,1'b0},{1'b0,1'b0,1'b0}}),
    .I1({Mux2xArray3_Array2_OutBit_inst2_O[2],{Mux2xArray3_Array2_OutBit_inst2_O[1],Mux2xArray3_Array2_OutBit_inst2_O[0]}}),
    .S((1'b1 & (({1'b0,x[1:0]}) <= 3'h1)) & ((3'((3'(({1'b0,x[1:0]}) + 3'h2)) - 3'h1)) >= 3'h1)),
    .O(Mux2xArray3_Array2_OutBit_inst3_O)
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst4 (
    .I0({I[0][2],{I[0][1],I[0][0]}}),
    .I1({I[1][2],{I[1][1],I[1][0]}}),
    .S(magma_Bits_3_sub_inst4_out[0]),
    .O(Mux2xArray3_Array2_OutBit_inst4_O)
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst5 (
    .I0({{1'b0,1'b0,1'b0},{1'b0,1'b0,1'b0}}),
    .I1({Mux2xArray3_Array2_OutBit_inst4_O[2],{Mux2xArray3_Array2_OutBit_inst4_O[1],Mux2xArray3_Array2_OutBit_inst4_O[0]}}),
    .S((1'b1 & (({1'b0,x[1:0]}) <= 3'h2)) & ((3'((3'(({1'b0,x[1:0]}) + 3'h2)) - 3'h1)) >= 3'h2)),
    .O(Mux2xArray3_Array2_OutBit_inst5_O)
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst6 (
    .I0({I[0][2],{I[0][1],I[0][0]}}),
    .I1({I[1][2],{I[1][1],I[1][0]}}),
    .S(magma_Bits_3_sub_inst6_out[0]),
    .O(Mux2xArray3_Array2_OutBit_inst6_O)
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst7 (
    .I0({{1'b0,1'b0,1'b0},{1'b0,1'b0,1'b0}}),
    .I1({Mux2xArray3_Array2_OutBit_inst6_O[2],{Mux2xArray3_Array2_OutBit_inst6_O[1],Mux2xArray3_Array2_OutBit_inst6_O[0]}}),
    .S(1'b1 & ((3'((3'(({1'b0,x[1:0]}) + 3'h2)) - 3'h1)) >= 3'h3)),
    .O(Mux2xArray3_Array2_OutBit_inst7_O)
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst8 (
    .I0({I[0][2],{I[0][1],I[0][0]}}),
    .I1({I[1][2],{I[1][1],I[1][0]}}),
    .S(magma_Bits_3_sub_inst8_out[0]),
    .O(Mux2xArray3_Array2_OutBit_inst8_O)
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst9 (
    .I0({{1'b0,1'b0,1'b0},{1'b0,1'b0,1'b0}}),
    .I1({Mux2xArray3_Array2_OutBit_inst8_O[2],{Mux2xArray3_Array2_OutBit_inst8_O[1],Mux2xArray3_Array2_OutBit_inst8_O[0]}}),
    .S(1'b1 & ((3'((3'(({1'b0,x[1:0]}) + 3'h2)) - 3'h1)) >= 3'h4)),
    .O(Mux2xArray3_Array2_OutBit_inst9_O)
);
assign magma_Bits_3_sub_inst0_out = 3'(3'h0 - ({1'b0,x[1:0]}));
assign magma_Bits_3_sub_inst10_out = 3'(3'h5 - ({1'b0,x[1:0]}));
assign magma_Bits_3_sub_inst2_out = 3'(3'h1 - ({1'b0,x[1:0]}));
assign magma_Bits_3_sub_inst4_out = 3'(3'h2 - ({1'b0,x[1:0]}));
assign magma_Bits_3_sub_inst6_out = 3'(3'h3 - ({1'b0,x[1:0]}));
assign magma_Bits_3_sub_inst8_out = 3'(3'h4 - ({1'b0,x[1:0]}));
assign O = {{{Mux2xArray3_Array2_OutBit_inst11_O[2],Mux2xArray3_Array2_OutBit_inst11_O[1],Mux2xArray3_Array2_OutBit_inst11_O[0]},{Mux2xArray3_Array2_OutBit_inst9_O[2],Mux2xArray3_Array2_OutBit_inst9_O[1],Mux2xArray3_Array2_OutBit_inst9_O[0]},{Mux2xArray3_Array2_OutBit_inst7_O[2],Mux2xArray3_Array2_OutBit_inst7_O[1],Mux2xArray3_Array2_OutBit_inst7_O[0]}},{{Mux2xArray3_Array2_OutBit_inst5_O[2],Mux2xArray3_Array2_OutBit_inst5_O[1],Mux2xArray3_Array2_OutBit_inst5_O[0]},{Mux2xArray3_Array2_OutBit_inst3_O[2],Mux2xArray3_Array2_OutBit_inst3_O[1],Mux2xArray3_Array2_OutBit_inst3_O[0]},{Mux2xArray3_Array2_OutBit_inst1_O[2],Mux2xArray3_Array2_OutBit_inst1_O[1],Mux2xArray3_Array2_OutBit_inst1_O[0]}}};
endmodule

