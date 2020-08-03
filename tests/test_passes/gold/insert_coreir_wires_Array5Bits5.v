module Main (
    input [4:0] I [4:0],
    output [4:0] O [4:0]
);
wire [24:0] x;
assign x = {I[4][4:0],I[3][4:0],I[2][4:0],I[1][4:0],I[0][4:0]};
assign O = '{x[24:20],x[19:15],x[14:10],x[9:5],x[4:0]};
endmodule

