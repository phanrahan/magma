module Foo (
    input [1:0] I [1:0],
    output [1:0] O [1:0]
);
assign O[1] = I[1];
assign O[0] = I[1];
endmodule

