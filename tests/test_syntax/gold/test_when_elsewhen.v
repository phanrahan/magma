module ConditionalDriver (
    input I0,
    input C0,
    input I1,
    input C1,
    input I2,
    input C2,
    output O
);
always @(*) begin
    if (C0) assign O = I0;
    else if (C1) assign O = I1;
    else if (C2) assign O = I2;
end
endmodule

module Foo (
    input [2:0] I,
    input [1:0] S,
    output O
);
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
ConditionalDriver ConditionalDriver_inst0 (
    .I0(I[0]),
    .C0(S[0]),
    .I1(I[1]),
    .C1(magma_Bit_and_inst0_out),
    .I2(I[2]),
    .C2(magma_Bit_and_inst1_out),
    .O(O)
);
assign magma_Bit_and_inst0_out = (~ S[0]) & S[1];
assign magma_Bit_and_inst1_out = (~ S[1]) & (~ S[0]);
endmodule

