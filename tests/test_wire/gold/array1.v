module main (output  O);
wire  a_O;
AndN2 a (.I(2'd2'), .O(a_O));
assign O = a_O;
endmodule

