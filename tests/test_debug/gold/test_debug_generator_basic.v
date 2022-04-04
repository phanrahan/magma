module Foo (
    input [3:0] I,
    output O
);
wire [3:0] x;
assign x = ~ I;
assign O = ^ x;
endmodule

