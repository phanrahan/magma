module And2 (input [1:0] I, output  O);
wire  inst0_O;
And2 inst0 (.I0(I[0]), .I1(I[1]), .O(inst0_O));
assign O = inst0_O;
endmodule

module main (input  I0, input  I1, output  O);
wire  inst0_O;
And2 inst0 (.I({I1,I0}), .O(inst0_O));
assign O = inst0_O;
endmodule

