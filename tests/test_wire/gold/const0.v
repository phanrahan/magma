module main (output  O);
wire  inst0_O;
Buf inst0 (.I(1'b0), .O(inst0_O));
assign O = inst0_O;
endmodule

