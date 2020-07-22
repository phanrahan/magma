module Main (
    input [4:0] I_0,
    input [4:0] I_1,
    input [4:0] I_2,
    output [2:0] O_0,
    output [2:0] O_1,
    output [2:0] O_2,
    output [2:0] O_3,
    output [2:0] O_4
);
assign O_0 = {I_2[0],I_1[0],I_0[0]};
assign O_1 = {I_2[1],I_1[1],I_0[1]};
assign O_2 = {I_2[2],I_1[2],I_0[2]};
assign O_3 = {I_2[3],I_1[3],I_0[3]};
assign O_4 = {I_2[4],I_1[4],I_0[4]};
endmodule

