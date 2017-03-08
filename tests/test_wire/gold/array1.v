module main (output  O);
wire  inst0_O;
AndN2 inst0 (.I({1'b1,1'b0}), .O(inst0_O));
assign O = inst0_O;
endmodule

