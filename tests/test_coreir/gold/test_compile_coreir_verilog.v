// Module `And2` defined externally
module main (input [1:0] I, output O);
wire and2_O;
And2 and2(.I0(I[0]), .I1(I[1]), .O(and2_O));
assign O = and2_O;
endmodule

