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
    input S,
    output O
);
ConditionalDriver ConditionalDriver_inst0 (
    .I0(I[0]),
    .C0(S),
    .I1(I[1]),
    .O(O)
);
endmodule

