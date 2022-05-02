module ConditionalDriver (
    input I0,
    input C0,
    input I1,
    input C1,
    output O
);
always @(*) begin
    if (C0) assign O = I0;
    else if (C1) assign O = I1;
end
endmodule

module Foo (
    input [1:0] I,
    input S,
    output O
);
wire magma_Bit_not_inst0_out;
ConditionalDriver ConditionalDriver_inst0 (
    .I0(I[0]),
    .C0(S),
    .I1(I[1]),
    .C1(magma_Bit_not_inst0_out),
    .O(O)
);
assign magma_Bit_not_inst0_out = ~ S;
endmodule

