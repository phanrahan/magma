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

module basic_if (
    input [1:0] I,
    input S,
    output O
);
wire __0_return_0;
wire __0_return_1;
wire _cond_0;
Mux2xBit Mux2xBit_inst0 (
    .I0(__0_return_1),
    .I1(__0_return_0),
    .S(_cond_0),
    .O(O)
);
assign __0_return_0 = I[0];
assign __0_return_1 = I[1];
assign _cond_0 = S;
endmodule

module Main (
    input [1:0] I,
    input S,
    output O
);
basic_if basic_if_inst0 (
    .I(I),
    .S(S),
    .O(O)
);
endmodule

