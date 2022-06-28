module _Foo (
    input [9:0][11:0][31:0] I,
    output [31:0] O
);
assign O = I[4][7];
endmodule

