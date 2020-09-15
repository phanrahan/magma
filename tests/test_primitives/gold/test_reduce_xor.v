module test_reduce_xor (
    input [4:0] I,
    output O0,
    output O1
);
assign O0 = ^ I;
assign O1 = ^ I;
endmodule

