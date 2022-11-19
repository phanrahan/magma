// Module `Foo` defined externally
module Main (
    input I,
    output O,
    input clocks_clk,
    input clocks_rst
);
wire foo_O;
Foo foo (
    .I(I),
    .O(foo_O),
    .clocks_clk(clocks_clk),
    .clocks_rst(clocks_rst)
);
assign O = foo_O;
endmodule

