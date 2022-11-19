module Main (
    input [1:0] I,
    output [1:0] O0,
    output [1:0] O1
);
wire [1:0] x_0;
wire [1:0] x_1;
wire y;
wire z;
assign x_0 = {z,y};
assign x_1 = {y,z};
assign y = I[1];
assign z = I[0];
assign O0 = {x_1[0],x_0[0]};
assign O1 = {x_0[1],x_1[1]};
endmodule

