module ConditionalDrivers (
    input C0,
    input C0I0
);
always @(*) begin
    if (C0) begin
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
    .C0I0(I[0])
);
assign O = I[1];
endmodule

