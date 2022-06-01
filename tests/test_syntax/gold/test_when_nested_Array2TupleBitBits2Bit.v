module ConditionalDriversImpl (
    input C0,
    input C0I0_0__0,
    input [1:0] C0I0_0__1,
    input C0I0_1__0,
    input [1:0] C0I0_1__1,
    input O0None_0__0,
    input [1:0] O0None_0__1,
    input O0None_1__0,
    input [1:0] O0None_1__1,
    output O0_0__0,
    output [1:0] O0_0__1,
    output O0_1__0,
    output [1:0] O0_1__1
);
reg  O0_0__0_reg;
reg [1:0] O0_0__1_reg;
reg  O0_1__0_reg;
reg [1:0] O0_1__1_reg;
always @(*) begin
    O0_0__0_reg = O0None_0__0;
    O0_0__1_reg = O0None_0__1;
    O0_1__0_reg = O0None_1__0;
    O0_1__1_reg = O0None_1__1;
    if (C0) begin
        O0_0__0_reg = C0I0_0__0;
        O0_0__1_reg = C0I0_0__1;
        O0_1__0_reg = C0I0_1__0;
        O0_1__1_reg = C0I0_1__1;
    end
end
assign O0_0__0 = O0_0__0_reg;
assign O0_0__1 = O0_0__1_reg;
assign O0_1__0 = O0_1__0_reg;
assign O0_1__1 = O0_1__1_reg;

endmodule

module Foo (
    input I_0_0__0,
    input [1:0] I_0_0__1,
    input I_0_1__0,
    input [1:0] I_0_1__1,
    input I_1_0__0,
    input [1:0] I_1_0__1,
    input I_1_1__0,
    input [1:0] I_1_1__1,
    output O_0__0,
    output [1:0] O_0__1,
    output O_1__0,
    output [1:0] O_1__1,
    input S
);
ConditionalDriversImpl ConditionalDriversImpl_inst0 (
    .C0(S),
    .C0I0_0__0(I_0_0__0),
    .C0I0_0__1(I_0_0__1),
    .C0I0_1__0(I_0_1__0),
    .C0I0_1__1(I_0_1__1),
    .O0None_0__0(I_1_0__0),
    .O0None_0__1(I_1_0__1),
    .O0None_1__0(I_1_1__0),
    .O0None_1__1(I_1_1__1),
    .O0_0__0(O_0__0),
    .O0_0__1(O_0__1),
    .O0_1__0(O_1__0),
    .O0_1__1(O_1__1)
);
endmodule

