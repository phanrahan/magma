module Main (
    input [1:0] I,
    output [1:0] O0,
    output [1:0] O1
);
wire [1:0] x_0;
wire [1:0] x_1;
assign x_0 = I;
assign x_1 = I;
assign O0 = x_0;
assign O1 = x_1;
endmodule

