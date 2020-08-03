// Module `Foo` defined externally
module Main (
    input [4:0] I [4:0],
    output [4:0] O [4:0]
);
wire [4:0] Foo_inst0_I [4:0];
wire [4:0] Foo_inst0_O [4:0];
wire [24:0] x;
assign Foo_inst0_I = '{I[4],I[3],I[2],I[1],I[0]};
Foo Foo_inst0 (
    .I(Foo_inst0_I),
    .O(Foo_inst0_O)
);
assign x = {Foo_inst0_O[4][4:0],Foo_inst0_O[3][4:0],Foo_inst0_O[2][4:0],Foo_inst0_O[1][4:0],Foo_inst0_O[0][4:0]};
assign O = '{x[24:20],x[19:15],x[14:10],x[9:5],x[4:0]};
endmodule

