module ConditionalDriversImpl (
    input C0,
    input C0I0,
    output O0,
    input O0None
);
reg  O0_reg;
always @(*) begin
    O0_reg = O0None;
    if (C0) begin
        O0_reg = C0I0;
    end
end
assign O0 = O0_reg;

endmodule

module Foo (
    input [1:0] I,
    input S,
    output O
);
ConditionalDriversImpl ConditionalDriversImpl_inst0 (
    .C0(S),
    .C0I0(I[0]),
    .O0(O),
    .O0None(I[1])
);
endmodule

