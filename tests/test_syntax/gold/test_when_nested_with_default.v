module ConditionalDriver (
    input I0,
    input C0,
    input I1,
    output O
);
always @(*) begin
    if (C0) assign O = I0;
    else assign O = I1;
end
endmodule

module Foo (
    input [1:0] I,
    input [1:0] S,
    output O
);
wire magma_Bit_and_inst0_out;
ConditionalDriver ConditionalDriver_inst0 (
    .I0(I[0]),
    .C0(magma_Bit_and_inst0_out),
    .I1(I[1]),
    .O(O)
);
assign magma_Bit_and_inst0_out = S[0] & S[1];
endmodule

