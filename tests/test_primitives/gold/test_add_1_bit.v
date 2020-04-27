module test_add_1_bit (
    input [4:0] I,
    input C,
    output [4:0] O
);
assign O = 5'(({1'b0,1'b0,1'b0,1'b0,C}) + I);
endmodule

