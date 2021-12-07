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
Mux2xBit Mux2xBit_inst0 (
    .I0(1'b0),
    .I1(1'b1),
    .S(s),
    .O(O1)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(1'b0),
    .I1(1'b1),
    .S(s),
    .O(O2)
);
Mux2xBits2 Mux2xBits2_inst0 (
    .I0(2'h1),
    .I1(2'h2),
    .S(s),
    .O(O0)
);
endmodule

