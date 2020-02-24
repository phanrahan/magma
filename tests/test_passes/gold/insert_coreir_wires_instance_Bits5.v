// Module `Foo` defined externally
module Main (
    input [4:0] I,
    output [4:0] O
);
wire [4:0] Foo_inst0_O;
wire [4:0] x;
Foo Foo_inst0 (
    .I(I),
    .O(Foo_inst0_O)
);
assign x = Foo_inst0_O;
assign O = x;
endmodule

