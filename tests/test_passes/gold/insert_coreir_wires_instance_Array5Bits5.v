// Module `Foo` defined externally
module Main (
    input [4:0] I [4:0],
    output [4:0] O [4:0]
);
wire [4:0] foo_O [4:0];
wire [24:0] x;
wire [4:0] foo_I [4:0];
assign foo_I[4] = I[4];
assign foo_I[3] = I[3];
assign foo_I[2] = I[2];
assign foo_I[1] = I[1];
assign foo_I[0] = I[0];
Foo foo (
    .I(foo_I),
    .O(foo_O)
);
assign x = {foo_O[4],foo_O[3],foo_O[2],foo_O[1],foo_O[0]};
assign O[4] = {x[24],x[23],x[22],x[21],x[20]};
assign O[3] = {x[19],x[18],x[17],x[16],x[15]};
assign O[2] = {x[14],x[13],x[12],x[11],x[10]};
assign O[1] = {x[9],x[8],x[7],x[6],x[5]};
assign O[0] = {x[4],x[3],x[2],x[1],x[0]};
endmodule

