module mantle_wire__typeBitIn6 (
    output [5:0] in,
    input [5:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBitIn2 (
    output [1:0] in,
    input [1:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit6 (
    input [5:0] in,
    output [5:0] out
);
assign out = in;
endmodule

module mantle_wire__typeBit2 (
    input [1:0] in,
    output [1:0] out
);
assign out = in;
endmodule

module Mux2xArray3_Array2_OutBit (
    input [1:0] I0_0,
    input [1:0] I0_1,
    input [1:0] I0_2,
    input [1:0] I1_0,
    input [1:0] I1_1,
    input [1:0] I1_2,
    output [1:0] O_0,
    output [1:0] O_1,
    output [1:0] O_2,
    input S
);
reg [5:0] coreir_commonlib_mux2x6_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x6_inst0_out = {I0_2[1:0],I0_1[1:0],I0_0[1:0]};
end else begin
    coreir_commonlib_mux2x6_inst0_out = {I1_2[1:0],I1_1[1:0],I1_0[1:0]};
end
end

assign O_0 = coreir_commonlib_mux2x6_inst0_out[1:0];
assign O_1 = coreir_commonlib_mux2x6_inst0_out[3:2];
assign O_2 = coreir_commonlib_mux2x6_inst0_out[5:4];
endmodule

module Mux2xArray3_Array2_Bit (
    input [1:0] I0_0,
    input [1:0] I0_1,
    input [1:0] I0_2,
    input [1:0] I1_0,
    input [1:0] I1_1,
    input [1:0] I1_2,
    output [1:0] O_0,
    output [1:0] O_1,
    output [1:0] O_2,
    input S
);
reg [5:0] coreir_commonlib_mux2x6_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x6_inst0_out = {I0_2[1:0],I0_1[1:0],I0_0[1:0]};
end else begin
    coreir_commonlib_mux2x6_inst0_out = {I1_2[1:0],I1_1[1:0],I1_0[1:0]};
end
end

assign O_0 = coreir_commonlib_mux2x6_inst0_out[1:0];
assign O_1 = coreir_commonlib_mux2x6_inst0_out[3:2];
assign O_2 = coreir_commonlib_mux2x6_inst0_out[5:4];
endmodule

module Main (
    input [1:0] I_0_0,
    input [1:0] I_0_1,
    input [1:0] I_0_2,
    input [1:0] I_1_0,
    input [1:0] I_1_1,
    input [1:0] I_1_2,
    output [1:0] O_0_0,
    output [1:0] O_0_1,
    output [1:0] O_0_2,
    output [1:0] O_1_0,
    output [1:0] O_1_1,
    output [1:0] O_1_2,
    output [1:0] O_2_0,
    output [1:0] O_2_1,
    output [1:0] O_2_2,
    output [1:0] O_3_0,
    output [1:0] O_3_1,
    output [1:0] O_3_2,
    output [1:0] O_4_0,
    output [1:0] O_4_1,
    output [1:0] O_4_2,
    output [1:0] O_5_0,
    output [1:0] O_5_1,
    output [1:0] O_5_2,
    input [1:0] x
);
wire [1:0] Mux2xArray3_Array2_OutBit_inst0_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst0_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst0_O_2;
wire [1:0] Mux2xArray3_Array2_OutBit_inst1_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst1_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst1_O_2;
wire [1:0] Mux2xArray3_Array2_OutBit_inst2_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst2_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst2_O_2;
wire [1:0] Mux2xArray3_Array2_OutBit_inst3_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst3_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst3_O_2;
wire [1:0] Mux2xArray3_Array2_OutBit_inst4_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst4_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst4_O_2;
wire [1:0] Mux2xArray3_Array2_OutBit_inst5_O_0;
wire [1:0] Mux2xArray3_Array2_OutBit_inst5_O_1;
wire [1:0] Mux2xArray3_Array2_OutBit_inst5_O_2;
wire [2:0] magma_Bits_3_sub_inst0_out;
wire [2:0] magma_Bits_3_sub_inst10_out;
wire [2:0] magma_Bits_3_sub_inst2_out;
wire [2:0] magma_Bits_3_sub_inst4_out;
wire [2:0] magma_Bits_3_sub_inst6_out;
wire [2:0] magma_Bits_3_sub_inst8_out;
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst0 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst0_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst0_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst0_O_2),
    .O_0(O_0_0),
    .O_1(O_0_1),
    .O_2(O_0_2),
    .S(1'b1 & (({1'b0,x[1:0]}) <= 3'h0))
);
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst1 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst1_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst1_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst1_O_2),
    .O_0(O_1_0),
    .O_1(O_1_1),
    .O_2(O_1_2),
    .S((1'b1 & (({1'b0,x[1:0]}) <= 3'h1)) & ((3'((3'(({1'b0,x[1:0]}) + 3'h2)) - 3'h1)) >= 3'h1))
);
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst2 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst2_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst2_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst2_O_2),
    .O_0(O_2_0),
    .O_1(O_2_1),
    .O_2(O_2_2),
    .S((1'b1 & (({1'b0,x[1:0]}) <= 3'h2)) & ((3'((3'(({1'b0,x[1:0]}) + 3'h2)) - 3'h1)) >= 3'h2))
);
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst3 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst3_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst3_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst3_O_2),
    .O_0(O_3_0),
    .O_1(O_3_1),
    .O_2(O_3_2),
    .S(1'b1 & ((3'((3'(({1'b0,x[1:0]}) + 3'h2)) - 3'h1)) >= 3'h3))
);
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst4 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst4_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst4_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst4_O_2),
    .O_0(O_4_0),
    .O_1(O_4_1),
    .O_2(O_4_2),
    .S(1'b1 & ((3'((3'(({1'b0,x[1:0]}) + 3'h2)) - 3'h1)) >= 3'h4))
);
Mux2xArray3_Array2_Bit Mux2xArray3_Array2_Bit_inst5 (
    .I0_0({1'b0,1'b0}),
    .I0_1({1'b0,1'b0}),
    .I0_2({1'b0,1'b0}),
    .I1_0(Mux2xArray3_Array2_OutBit_inst5_O_0),
    .I1_1(Mux2xArray3_Array2_OutBit_inst5_O_1),
    .I1_2(Mux2xArray3_Array2_OutBit_inst5_O_2),
    .O_0(O_5_0),
    .O_1(O_5_1),
    .O_2(O_5_2),
    .S(1'b1 & ((3'((3'(({1'b0,x[1:0]}) + 3'h2)) - 3'h1)) >= 3'h5))
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst0 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst0_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst0_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst0_O_2),
    .S(magma_Bits_3_sub_inst0_out[0])
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst1 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst1_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst1_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst1_O_2),
    .S(magma_Bits_3_sub_inst2_out[0])
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst2 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst2_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst2_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst2_O_2),
    .S(magma_Bits_3_sub_inst4_out[0])
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst3 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst3_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst3_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst3_O_2),
    .S(magma_Bits_3_sub_inst6_out[0])
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst4 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst4_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst4_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst4_O_2),
    .S(magma_Bits_3_sub_inst8_out[0])
);
Mux2xArray3_Array2_OutBit Mux2xArray3_Array2_OutBit_inst5 (
    .I0_0(I_0_0),
    .I0_1(I_0_1),
    .I0_2(I_0_2),
    .I1_0(I_1_0),
    .I1_1(I_1_1),
    .I1_2(I_1_2),
    .O_0(Mux2xArray3_Array2_OutBit_inst5_O_0),
    .O_1(Mux2xArray3_Array2_OutBit_inst5_O_1),
    .O_2(Mux2xArray3_Array2_OutBit_inst5_O_2),
    .S(magma_Bits_3_sub_inst10_out[0])
);
assign magma_Bits_3_sub_inst0_out = 3'(3'h0 - ({1'b0,x[1:0]}));
assign magma_Bits_3_sub_inst10_out = 3'(3'h5 - ({1'b0,x[1:0]}));
assign magma_Bits_3_sub_inst2_out = 3'(3'h1 - ({1'b0,x[1:0]}));
assign magma_Bits_3_sub_inst4_out = 3'(3'h2 - ({1'b0,x[1:0]}));
assign magma_Bits_3_sub_inst6_out = 3'(3'h3 - ({1'b0,x[1:0]}));
assign magma_Bits_3_sub_inst8_out = 3'(3'h4 - ({1'b0,x[1:0]}));
endmodule

