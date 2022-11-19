module main (input [1:0] I0, input [1:0] I1, output [1:0] O);
wire [1:0] and2_O;
And2 and2 (.I0(I0), .I1(I1), .O(and2_O));
assign O = and2_O;
endmodule

