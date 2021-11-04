module Foo (
    input I__0,
    input [1:0] I__1,
    output O__0,
    output [1:0] O__1
);
assign O__0 = I__0;
assign O__1 = {I__1[0],I__1[1]};
endmodule

