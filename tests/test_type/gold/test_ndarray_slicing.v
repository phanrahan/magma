module Main (
    output [2:0] a0 [3:0][4:0],
    output [2:0] a1 [3:0][4:0],
    input [2:0] b [1:0][4:0],
    input [1:0] c [2:0]
);
assign a0[3][4] = {1'b0,1'b0,1'b1};
assign a0[3][3] = {1'b0,1'b0,1'b1};
assign a0[3][2] = {1'b0,1'b0,1'b1};
assign a0[3][1] = {1'b0,1'b0,1'b1};
assign a0[3][0] = {1'b0,1'b0,1'b1};
assign a0[2][4] = {1'b0,1'b0,1'b0};
assign a0[2][3] = {1'b0,1'b0,1'b0};
assign a0[2][2] = {1'b0,1'b0,1'b0};
assign a0[2][1] = {1'b0,1'b0,1'b0};
assign a0[2][0] = {1'b0,1'b0,1'b0};
assign a0[1][4] = b[1][4];
assign a0[1][3] = b[1][3];
assign a0[1][2] = b[1][2];
assign a0[1][1] = b[1][1];
assign a0[1][0] = b[1][0];
assign a0[0][4] = b[0][4];
assign a0[0][3] = b[0][3];
assign a0[0][2] = b[0][2];
assign a0[0][1] = b[0][1];
assign a0[0][0] = b[0][0];
assign a1[3][4] = {1'b0,1'b0,1'b0};
assign a1[3][3] = {1'b0,1'b0,1'b0};
assign a1[3][2] = {1'b0,1'b0,1'b0};
assign a1[3][1] = {1'b0,1'b0,1'b0};
assign a1[3][0] = {1'b1,1'b0,1'b0};
assign a1[2][4] = {1'b0,c[2]};
assign a1[2][3] = {1'b0,c[1]};
assign a1[2][2] = {1'b0,c[0]};
assign a1[2][1] = {1'b0,1'b0,1'b0};
assign a1[2][0] = {1'b1,1'b0,1'b0};
assign a1[1][4] = {1'b0,1'b0,1'b0};
assign a1[1][3] = {1'b0,1'b0,1'b0};
assign a1[1][2] = {1'b0,1'b0,1'b0};
assign a1[1][1] = {1'b0,1'b0,1'b0};
assign a1[1][0] = {1'b1,1'b0,1'b0};
assign a1[0][4] = {1'b0,1'b0,1'b0};
assign a1[0][3] = {1'b0,1'b0,1'b0};
assign a1[0][2] = {1'b0,1'b0,1'b0};
assign a1[0][1] = {1'b0,1'b0,1'b0};
assign a1[0][0] = {1'b1,1'b0,1'b0};
endmodule

