module same (input  I, output  O);
assign O = I;
endmodule

module test (input  I, output  O1, output  O2);
wire  inst0_O;
wire  inst1_O;
same inst0 (.I(I), .O(inst0_O));
same inst1 (.I(I), .O(inst1_O));
assign O1 = inst0_O;
assign O2 = inst1_O;
endmodule

