module main (input [1:0] I, output  O);
wire  a_O;
AndN2 a (.I(I), .O(a_O));
assign O = a_O;
endmodule

