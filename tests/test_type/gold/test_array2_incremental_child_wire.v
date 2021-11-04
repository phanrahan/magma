module Foo (
    input I_0__0,
    input [1:0] I_0__1,
    input I_1__0,
    input [1:0] I_1__1,
    input I_2__0,
    input [1:0] I_2__1,
    input I_3__0,
    input [1:0] I_3__1,
    output O_0__0,
    output [1:0] O_0__1,
    output O_1__0,
    output [1:0] O_1__1,
    output O_2__0,
    output [1:0] O_2__1,
    output O_3__0,
    output [1:0] O_3__1
);
assign O_0__0 = I_3__0;
assign O_0__1 = I_0__1;
assign O_1__0 = I_2__0;
assign O_1__1 = I_1__1;
assign O_2__0 = I_1__0;
assign O_2__1 = I_2__1;
assign O_3__0 = I_0__0;
assign O_3__1 = I_3__1;
endmodule

