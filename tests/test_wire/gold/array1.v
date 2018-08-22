module main (output  O);
wire  inst0_O;
AndN2 inst0 (.I(2'h2), .O(inst0_O));
assign O = inst0_O;
endmodule

