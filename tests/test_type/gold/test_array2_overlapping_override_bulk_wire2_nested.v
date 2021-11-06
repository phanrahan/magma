module Foo (
    input [3:0] I [3:0],
    output [3:0] O [3:0]
);
assign O[3] = I[3];
assign O[2] = I[2];
assign O[1] = I[1];
assign O[0] = I[0];
endmodule

