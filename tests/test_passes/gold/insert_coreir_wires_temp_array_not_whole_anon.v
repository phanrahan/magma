module Main (
    input [1:0] I,
    output [1:0] O0,
    output [1:0] O1
);
wire y;
wire z;
assign y = I[1];
assign z = I[0];
assign O0 = {z,y};
assign O1 = {z,y};
endmodule

