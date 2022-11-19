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
wire foo_y;
Foo foo (
    .x(I),
    .y(foo_y)
);
assign O = foo_y;
endmodule


`endif