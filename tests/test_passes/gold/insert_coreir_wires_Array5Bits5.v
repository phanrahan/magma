module Main (
    input [4:0] I_0,
    input [4:0] I_1,
    input [4:0] I_2,
    input [4:0] I_3,
    input [4:0] I_4,
    output [4:0] O_0,
    output [4:0] O_1,
    output [4:0] O_2,
    output [4:0] O_3,
    output [4:0] O_4
);
wire [24:0] x;
assign x = {I_4[4:0],I_3[4:0],I_2[4:0],I_1[4:0],I_0[4:0]};
assign O_0 = x[4:0];
assign O_1 = x[9:5];
assign O_2 = x[14:10];
assign O_3 = x[19:15];
assign O_4 = x[24:20];
endmodule

