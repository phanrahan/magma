module Register2 (input [1:0] I, output [1:0] O, input  CLK);
wire  inst0_O;
wire  inst1_O;
DFF inst0 (.I(I[0]), .O(inst0_O), .CLK(CLK));
DFF inst1 (.I(I[1]), .O(inst1_O), .CLK(CLK));
assign O = {inst1_O,inst0_O};
endmodule

module main (input  CLK, input [1:0] I, output [1:0] O);
wire [1:0] inst0_O;
Register2 inst0 (.I(I), .O(inst0_O), .CLK(CLK));
assign O = inst0_O;
endmodule

