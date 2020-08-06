module Main (
    input [2:0] I [4:0],
    output [4:0] O [2:0]
);
assign O[2] = {I[4][2],I[3][2],I[2][2],I[1][2],I[0][2]};
assign O[1] = {I[4][1],I[3][1],I[2][1],I[1][1],I[0][1]};
assign O[0] = {I[4][0],I[3][0],I[2][0],I[1][0],I[0][0]};
endmodule

