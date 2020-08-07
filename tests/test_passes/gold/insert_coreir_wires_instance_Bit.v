// Module `Foo` defined externally
module Main (
    input I,
    output O
);
wire Foo_inst0_I;
wire Foo_inst0_O;
wire x;
assign Foo_inst0_I = I;
Foo Foo_inst0 (
    .I(Foo_inst0_I),
    .O(Foo_inst0_O)
);
assign x = Foo_inst0_O;
assign O = x;
endmodule

