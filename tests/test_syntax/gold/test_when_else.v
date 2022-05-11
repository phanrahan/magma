module ConditionalDrivers (
    input C0,
    input C0I0,
    input C1I0,
    output O0
);
always @(*) begin
    if (C0) begin
        O0 = C0I0;
    end else begin
        O0 = C1I0;
    end
end
endmodule

module Foo (
    input [1:0] I,
    input S,
    output O
);
ConditionalDrivers ConditionalDrivers_inst0 (
    .C0(S),
    .C0I0(I[0]),
    .C1I0(I[1]),
    .O0(O)
);
endmodule

