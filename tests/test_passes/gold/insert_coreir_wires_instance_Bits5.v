// Module `Foo` defined externally
module Main (
    input [4:0] I,
    output [4:0] O
);
wire [4:0] foo_O;
wire [4:0] x;
Foo foo (
    .I(I),
    .O(foo_O)
);
assign x = foo_O;
assign O = x;
endmodule

