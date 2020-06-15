module pre_unroll (
    input [2:0] I,
    output [2:0] O
);
assign O = I[0] ? 3'h0 : I[1] ? 3'h1 : I[2] ? 3'h2 : 3'h4;
endmodule

