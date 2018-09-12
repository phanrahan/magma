module main (output [0:0] O);
wire [0:0] inst0_O;
Buf inst0 (.I({1'b1}), .O(inst0_O));
assign O = inst0_O;
endmodule

