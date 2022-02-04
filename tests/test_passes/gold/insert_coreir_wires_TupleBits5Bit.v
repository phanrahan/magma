module Main (
    input [4:0] I__0,
    input I__1,
    output [4:0] O__0,
    output O__1
);
wire [5:0] x;
assign x = {I__1,I__0};
assign O__0 = {x[4],x[3],x[2],x[1],x[0]};
assign O__1 = x[5];
endmodule

