module TestRepeat (
    input [2:0] I,
    output [20:0] O
);
assign O = {I,I,I,I,I,I,I};
endmodule

