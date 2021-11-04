module Foo (
    input [3:0] I,
    output [3:0] O
);
assign O = {I[1:0],I[3:2]};
endmodule

