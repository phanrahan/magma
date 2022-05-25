module ConditionalDriversImpl (
    input C0,
    input C0I0,
    input C1,
    input C1I0,
    input C2I0,
    output O0
);
reg  O0_reg;
always @(*) begin
    if (C0) begin
        O0_reg = C0I0;
    end else begin
        if (C1) begin
            O0_reg = C1I0;
        end else begin
            O0_reg = C2I0;
        end
    end
end
assign O0 = O0_reg;

endmodule

module Foo (
    input [2:0] I,
    input [1:0] S,
    output O
);
ConditionalDriversImpl ConditionalDriversImpl_inst0 (
    .C0(S[0]),
    .C0I0(I[0]),
    .C1(S[1]),
    .C1I0(I[1]),
    .C2I0(I[2]),
    .O0(O)
);
endmodule

