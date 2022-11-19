module main (input  I0, input  I1, output  O);
wire  and2_O;
And2 and2 (.I0(I0), .I1(I1), .O(and2_O));
assign O = and2_O;
endmodule

