module ConditionalDrivers (
    input C0,
    input C0I0,
    input C1,
    input C1I0,
    input C2I0,
    output O0
);
always @(*) begin
    if (C0) begin
        O0 = C0I0;
    end else begin
        if (C1) begin
            O0 = C1I0;
        end else begin
            O0 = C2I0;
        end
    end
end
endmodule

module Foo (
    input [2:0] I,
    input [1:0] S,
    output O
);
ConditionalDrivers ConditionalDrivers_inst0 (
    .C0(S[0]),
    .C0I0(I[0]),
    .C1(S[1]),
    .C1I0(I[1]),
    .C2I0(I[2]),
    .O0(O)
);
endmodule

