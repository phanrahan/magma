module main (input [1:0] I, output  O);
wire  inst0_O;
AndN2 inst0 (.I(I), .O(inst0_O));
assign O = inst0_O;
endmodule

