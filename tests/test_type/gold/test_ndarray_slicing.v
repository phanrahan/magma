module Main (
    output [3:0] a0_0_0,
    output [3:0] a0_0_1,
    output [3:0] a0_0_2,
    output [3:0] a0_0_3,
    output [3:0] a0_0_4,
    output [3:0] a0_1_0,
    output [3:0] a0_1_1,
    output [3:0] a0_1_2,
    output [3:0] a0_1_3,
    output [3:0] a0_1_4,
    output [3:0] a0_2_0,
    output [3:0] a0_2_1,
    output [3:0] a0_2_2,
    output [3:0] a0_2_3,
    output [3:0] a0_2_4,
    output [3:0] a1_0_0,
    output [3:0] a1_0_1,
    output [3:0] a1_0_2,
    output [3:0] a1_0_3,
    output [3:0] a1_0_4,
    output [3:0] a1_1_0,
    output [3:0] a1_1_1,
    output [3:0] a1_1_2,
    output [3:0] a1_1_3,
    output [3:0] a1_1_4,
    output [3:0] a1_2_0,
    output [3:0] a1_2_1,
    output [3:0] a1_2_2,
    output [3:0] a1_2_3,
    output [3:0] a1_2_4,
    input [3:0] b_0_0,
    input [3:0] b_0_1,
    input [3:0] b_0_2,
    input [3:0] b_0_3,
    input [3:0] b_0_4,
    input [3:0] b_1_0,
    input [3:0] b_1_1,
    input [3:0] b_1_2,
    input [3:0] b_1_3,
    input [3:0] b_1_4,
    input [2:0] c_0,
    input [2:0] c_1
);
assign a0_0_0 = b_0_0;
assign a0_0_1 = b_0_1;
assign a0_0_2 = b_0_2;
assign a0_0_3 = b_0_3;
assign a0_0_4 = b_0_4;
assign a0_1_0 = b_1_0;
assign a0_1_1 = b_1_1;
assign a0_1_2 = b_1_2;
assign a0_1_3 = b_1_3;
assign a0_1_4 = b_1_4;
assign a0_2_0 = {1'b0,1'b0,1'b0,1'b0};
assign a0_2_1 = {1'b0,1'b0,1'b0,1'b0};
assign a0_2_2 = {1'b0,1'b0,1'b0,1'b0};
assign a0_2_3 = {1'b0,1'b0,1'b0,1'b0};
assign a0_2_4 = {1'b0,1'b0,1'b0,1'b0};
assign a1_0_0 = {1'b0,1'b0,1'b0,1'b0};
assign a1_0_1 = {1'b0,1'b0,1'b0,1'b0};
assign a1_0_2 = {1'b0,c_0[0],1'b0,1'b0};
assign a1_0_3 = {1'b0,c_0[1],1'b0,1'b0};
assign a1_0_4 = {1'b0,c_0[2],1'b0,1'b0};
assign a1_1_0 = {1'b0,1'b0,1'b0,1'b0};
assign a1_1_1 = {1'b0,1'b0,1'b0,1'b0};
assign a1_1_2 = {1'b0,c_1[0],1'b0,1'b0};
assign a1_1_3 = {1'b0,c_1[1],1'b0,1'b0};
assign a1_1_4 = {1'b0,c_1[2],1'b0,1'b0};
assign a1_2_0 = {1'b0,1'b0,1'b0,1'b0};
assign a1_2_1 = {1'b0,1'b0,1'b0,1'b0};
assign a1_2_2 = {1'b0,1'b0,1'b0,1'b0};
assign a1_2_3 = {1'b0,1'b0,1'b0,1'b0};
assign a1_2_4 = {1'b0,1'b0,1'b0,1'b0};
endmodule

