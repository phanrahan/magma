// Module `Foo` defined externally
module my_namespace_Main (
    input I,
    output O
);
wire Foo_inst0_I;
wire Foo_inst0_O;
assign Foo_inst0_I = I;
Foo Foo_inst0 (
    .I(Foo_inst0_I),
    .O(Foo_inst0_O)
);
assign O = Foo_inst0_O;
endmodule

