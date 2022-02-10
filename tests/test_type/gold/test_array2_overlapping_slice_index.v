module Foo (
    input [1:0] I,
    output [1:0] O
);
assign O = {I[1],I[1]};
endmodule

