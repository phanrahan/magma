// Module `Foo` defined externally
module corebit_wire (
    input in,
    output out
);
  assign out = in;
endmodule

module Main (
    input I,
    output O
);
wire Foo_inst0_O;
wire x_out;
Foo Foo_inst0 (
    .I(I),
    .O(Foo_inst0_O)
);
corebit_wire x (
    .in(Foo_inst0_O),
    .out(x_out)
);
assign O = x_out;
endmodule

