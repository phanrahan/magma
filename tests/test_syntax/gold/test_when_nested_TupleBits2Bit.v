module ConditionalDriversImpl (
    input C0,
    input [1:0] C0I0,
    input C0I1,
    output [1:0] O0,
    input [1:0] O0None,
    output O1,
    input O1None
);
reg [1:0] O0_reg;
reg  O1_reg;
always @(*) begin
    O0_reg = O0None;
    O1_reg = O1None;
    if (C0) begin
        O0_reg = C0I0;
        O1_reg = C0I1;
    end
end
assign O0 = O0_reg;
assign O1 = O1_reg;

endmodule

module Foo (
    input [1:0] I_0__0,
    input I_0__1,
    input [1:0] I_1__0,
    input I_1__1,
    output [1:0] O__0,
    output O__1,
    input S
);
ConditionalDriversImpl ConditionalDriversImpl_inst0 (
    .C0(S),
    .C0I0(I_0__0),
    .C0I1(I_0__1),
    .O0(O__0),
    .O0None(I_1__0),
    .O1(O__1),
    .O1None(I_1__1)
);
endmodule

