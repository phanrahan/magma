module Foo (
    input [3:0] I,
    output [1:0] O
);
assign O = {I[3],I[1]};
endmodule

