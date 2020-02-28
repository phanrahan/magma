module main (input  I0, input  I1, output  O);
wire  And2_inst0_O;
And2 And2_inst0 (.I0(I0), .I1(I1), .O(And2_inst0_O));
assign O = And2_inst0_O;
endmodule

