module main (input  I, output  O);
wire  inst0_O;
wire  inst1_O;
Buf inst0 (.I(I), .O(inst0_O));
Buf inst1 (.I(inst0_O), .O(inst1_O));
assign O = inst1_O;
endmodule

