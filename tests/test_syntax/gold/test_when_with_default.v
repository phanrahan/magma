module ConditionalDriversImpl (
    input C0,
    input C0I0,
    output O0,
    input O0None
);
always @(*) begin
    O0 = O0None;
    if (C0) begin
        O0 = C0I0;
    end
end
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

