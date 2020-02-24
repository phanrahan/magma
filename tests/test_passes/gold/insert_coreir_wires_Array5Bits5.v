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
assign x = {I_4[4],I_4[3],I_4[2],I_4[1],I_4[0],I_3[4],I_3[3],I_3[2],I_3[1],I_3[0],I_2[4],I_2[3],I_2[2],I_2[1],I_2[0],I_1[4],I_1[3],I_1[2],I_1[1],I_1[0],I_0[4],I_0[3],I_0[2],I_0[1],I_0[0]};
assign O_0 = {x[4],x[3],x[2],x[1],x[0]};
assign O_1 = {x[9],x[8],x[7],x[6],x[5]};
assign O_2 = {x[14],x[13],x[12],x[11],x[10]};
assign O_3 = {x[19],x[18],x[17],x[16],x[15]};
assign O_4 = {x[24],x[23],x[22],x[21],x[20]};
endmodule

