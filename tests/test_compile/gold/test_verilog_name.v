// Module `Foo` defined externally
module baz_Bar (
    input I,
    output O
);
wire Foo_inst0_O;
Foo Foo_inst0 (
    .I(I),
    .O(Foo_inst0_O)
);
assign O = Foo_inst0_O;
endmodule

