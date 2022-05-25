module ConditionalDriversImpl (
    input C0,
    input C1,
    input C1I0,
    output O0,
    input O0None
);
reg  O0_reg;
always @(*) begin
    O0_reg = O0None;
    if (C0) begin
        if (C1) begin
            O0_reg = C1I0;
        end
    end
end
assign O0 = O0_reg;

endmodule

module Foo (
    input [1:0] I,
    input [1:0] S,
    output O
);
ConditionalDriversImpl ConditionalDriversImpl_inst0 (
    .C0(S[0]),
    .C1(S[1]),
    .C1I0(I[0]),
    .O0(O),
    .O0None(I[1])
);
endmodule

