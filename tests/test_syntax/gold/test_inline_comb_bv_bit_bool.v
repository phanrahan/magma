module Mux2xBits2 (
    input [1:0] I0,
    input [1:0] I1,
    input S,
    output [1:0] O
);
reg [1:0] coreir_commonlib_mux2x2_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x2_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x2_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x2_inst0_out;
endmodule

module Mux2xBit (
    input I0,
    input I1,
    input S,
    output O
);
reg [0:0] coreir_commonlib_mux2x1_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x1_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x1_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module Main (
    input s,
    output [1:0] O0,
    output O1,
    output O2
);
wire bit_const_0_None_out;
wire bit_const_1_None_out;
wire [1:0] const_1_2_out;
wire [1:0] const_2_2_out;
Mux2xBit Mux2xBit_inst0 (
    .I0(bit_const_0_None_out),
    .I1(bit_const_1_None_out),
    .S(s),
    .O(O1)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(bit_const_0_None_out),
    .I1(bit_const_1_None_out),
    .S(s),
    .O(O2)
);
Mux2xBits2 Mux2xBits2_inst0 (
    .I0(const_1_2_out),
    .I1(const_2_2_out),
    .S(s),
    .O(O0)
);
assign bit_const_0_None_out = 1'b0;
assign bit_const_1_None_out = 1'b1;
assign const_1_2_out = 2'h1;
assign const_2_2_out = 2'h2;
endmodule

