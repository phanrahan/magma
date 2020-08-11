// Module `Foo` defined externally
module Main (
    input I,
    output O
);
wire Foo_inst0_O;
wire x;
Foo Foo_inst0 (
    .I(I),
    .O(Foo_inst0_O)
);
assign x = Foo_inst0_O;
assign O = x;
endmodule

