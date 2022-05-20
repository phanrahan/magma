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

module Foo (
    input [1:0] I,
    input S,
    output O
);
Mux2xBit Mux2xBit_inst0 (
    .I0(I[1]),
    .I1(I[0]),
    .S(S),
    .O(O)
);
endmodule

