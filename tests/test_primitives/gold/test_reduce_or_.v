module test_reduce_or_ (
    input [4:0] I,
    output O
);
assign O = | I;
endmodule

