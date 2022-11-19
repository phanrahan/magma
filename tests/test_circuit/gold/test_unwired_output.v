module main (input [1:0] I, output  O);
wire  and2_O;
And2 and2 (.I1(I[1]), .O(and2_O));
endmodule

