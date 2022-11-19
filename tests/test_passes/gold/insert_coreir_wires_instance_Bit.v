// Module `Foo` defined externally
module Main (
    input I,
    output O
);
wire foo_O;
wire x;
Foo foo (
    .I(I),
    .O(foo_O)
);
assign x = foo_O;
assign O = x;
endmodule

