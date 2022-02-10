module main (input [1:0] I0, input [1:0] I1, output [1:0] O);
wire [1:0] And2_inst0_O;
And2 And2_inst0 (.I0(I0), .I1(I1), .O(And2_inst0_O));
assign O = And2_inst0_O;
endmodule

