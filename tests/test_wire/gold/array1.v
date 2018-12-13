module main (output  O);
wire  AndN2_inst0_O;
AndN2 AndN2_inst0 (.I({1'b1,1'b0}), .O(AndN2_inst0_O));
assign O = AndN2_inst0_O;
endmodule

