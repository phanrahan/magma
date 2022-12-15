// Module `Foo` defined externally
module Main (
    input I,
    output O,
    input clocks_clk,
    input clocks_rst
);
wire Foo_inst0_O;
Foo Foo_inst0 (
    .I(I),
    .O(Foo_inst0_O),
    .clocks_clk(clocks_clk),
    .clocks_rst(clocks_rst)
);
assign O = Foo_inst0_O;
endmodule

