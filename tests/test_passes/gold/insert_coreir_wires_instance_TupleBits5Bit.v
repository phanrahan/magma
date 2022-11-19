// Module `Foo` defined externally
module Main (
    input [4:0] I__0,
    input I__1,
    output [4:0] O__0,
    output O__1
);
wire [4:0] foo_O__0;
wire foo_O__1;
wire [5:0] x;
Foo foo (
    .I__0(I__0),
    .I__1(I__1),
    .O__0(foo_O__0),
    .O__1(foo_O__1)
);
assign x = {foo_O__1,foo_O__0};
assign O__0 = {x[4],x[3],x[2],x[1],x[0]};
assign O__1 = x[5];
endmodule

