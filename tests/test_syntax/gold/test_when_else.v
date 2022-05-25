module ConditionalDriversImpl (
    input C0,
    input C0I0,
    input C1I0,
    output O0
);
reg  O0_reg;
always @(*) begin
    if (C0) begin
        O0_reg = C0I0;
    end else begin
        O0_reg = C1I0;
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
    .C1I0(I[1]),
    .O0(O)
);
endmodule

