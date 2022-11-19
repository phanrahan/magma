module main (input  I0, input  I1, output  O);
wire  a_O;
And2 a (.I0(I0), .I1(I1), .O(a_O));
assign O = a_O;
endmodule

