module main (input  I, output  O);
wire  inst0_O;
Buf inst0 (.I(I), .O(inst0_O));
assign O = inst0_O;
endmodule

