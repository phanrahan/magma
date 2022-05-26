module ConditionalDriversImpl (
    input C0,
    input C1,
    input C1I0,
    input C1I1,
    output O0,
    input O0None,
    output O1,
    input O1None
);
reg  O0_reg;
reg  O1_reg;
always @(*) begin
    O0_reg = O0None;
    O1_reg = O1None;
    if (C0) begin
        if (C1) begin
            O0_reg = O1None;
            O1_reg = O0None;
        end
    end
end
assign O0 = O0_reg;
assign O1 = O1_reg;

endmodule

module Foo (
    input [1:0] I,
    input [1:0] S,
    output O0,
    output O1
);
ConditionalDriversImpl ConditionalDriversImpl_inst0 (
    .C0(S[0]),
    .C1(S[1]),
    .C1I0(I[0]),
    .C1I1(I[1]),
    .O0(O0),
    .O0None(I[1]),
    .O1(O1),
    .O1None(I[0])
);
endmodule
