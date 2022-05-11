module ConditionalDrivers (
    input C0,
    input C1,
    input C1I0,
    input O0None,
    output O0
);
always @(*) begin
    O0 = O0None;
    if (C0) begin
    end else begin
        if (C1) begin
            O0 = C1I0;
        end
    end
end
endmodule

module Foo (
    input [1:0] I,
    input [1:0] S,
    output O
);
ConditionalDrivers ConditionalDrivers_inst0 (
    .C0(S[0]),
    .C1(S[1]),
    .C1I0(I[0]),
    .O0None(I[1]),
    .O0(O)
);
endmodule

