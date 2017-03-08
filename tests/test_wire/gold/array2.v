module main (input  I, output  O);
wire  inst0_O;
AndN2 inst0 (.I({1'b1,I}), .O(inst0_O));
assign O = inst0_O;
endmodule

