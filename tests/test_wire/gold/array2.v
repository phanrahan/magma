module main (input  I, output  O);
wire  a_O;
AndN2 a (.I({1'b1,I}), .O(a_O));
assign O = a_O;
endmodule

