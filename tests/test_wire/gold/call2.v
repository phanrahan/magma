module main (input [1:0] I, output  O);
wire  AndN2_inst0_O;
AndN2 AndN2_inst0 (.I(I), .O(AndN2_inst0_O));
assign O = AndN2_inst0_O;
endmodule

