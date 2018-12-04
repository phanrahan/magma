module main (input [1:0] I, output  O);
wire  And2_inst0_O;
And2 And2_inst0 (.I0(I[0]), .I1(I[1]), .O(And2_inst0_O));
assign O = And2_inst0_O;
endmodule

