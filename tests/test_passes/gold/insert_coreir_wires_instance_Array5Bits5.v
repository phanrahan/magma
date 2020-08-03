// Module `Foo` defined externally
module Main (
    input [4:0][4:0] I,
    output [4:0][4:0] O
);
wire [4:0][4:0] Foo_inst0_O;
wire [24:0] x;
Foo Foo_inst0 (
    .I({I[4],I[3],I[2],I[1],I[0]}),
    .O(Foo_inst0_O)
);
assign x = {Foo_inst0_O[4][4:0],Foo_inst0_O[3][4:0],Foo_inst0_O[2][4:0],Foo_inst0_O[1][4:0],Foo_inst0_O[0][4:0]};
assign O = {x[24:20],x[19:15],x[14:10],x[9:5],x[4:0]};
endmodule

