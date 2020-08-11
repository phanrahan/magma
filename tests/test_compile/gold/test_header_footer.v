/*
This is a test header, useful for something like a copyright that you'd like to
include in all your generated files
*/

`ifdef FOO
// Module `Foo` defined externally
module Main (
    input I,
    output O
);
wire Foo_inst0_y;
Foo Foo_inst0 (
    .x(I),
    .y(Foo_inst0_y)
);
assign O = Foo_inst0_y;
endmodule


`endif