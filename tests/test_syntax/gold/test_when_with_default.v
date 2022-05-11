module ConditionalDrivers (
    input C0,
    input C0I0,
    input O0None,
    output O0
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
ConditionalDrivers ConditionalDrivers_inst0 (
    .C0(S),
    .C0I0(I[0]),
    .O0None(I[1]),
    .O0(O)
);
endmodule

