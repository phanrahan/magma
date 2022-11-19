module main (input [1:0] I, output  O);
wire  a_O;
And2 a (.I0(I[0]), .I1(I[1]), .O(a_O));
assign O = a_O;
endmodule

