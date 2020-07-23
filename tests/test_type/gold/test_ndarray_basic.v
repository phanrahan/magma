module Main (
    input [2:0] I_0,
    input [2:0] I_1,
    input [2:0] I_2,
    input [2:0] I_3,
    input [2:0] I_4,
    output [4:0] O_0,
    output [4:0] O_1,
    output [4:0] O_2
);
assign O_0 = {I_4[0],I_3[0],I_2[0],I_1[0],I_0[0]};
assign O_1 = {I_4[1],I_3[1],I_2[1],I_1[1],I_0[1]};
assign O_2 = {I_4[2],I_3[2],I_2[2],I_1[2],I_0[2]};
endmodule

