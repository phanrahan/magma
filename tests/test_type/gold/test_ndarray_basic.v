module Main (
    input [4:0] I [2:0],
    output [2:0] O [4:0]
);
assign O[4] = {I[2][4],I[1][4],I[0][4]};
assign O[3] = {I[2][3],I[1][3],I[0][3]};
assign O[2] = {I[2][2],I[1][2],I[0][2]};
assign O[1] = {I[2][1],I[1][1],I[0][1]};
assign O[0] = {I[2][0],I[1][0],I[0][0]};
endmodule

