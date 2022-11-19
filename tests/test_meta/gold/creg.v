module Register2 (input [1:0] I, output [1:0] O, input  CLK);
wire  DFF_inst0_O;
wire  DFF_inst1_O;
DFF DFF_inst0 (.I(I[0]), .O(DFF_inst0_O), .CLK(CLK));
DFF DFF_inst1 (.I(I[1]), .O(DFF_inst1_O), .CLK(CLK));
assign O = {DFF_inst1_O,DFF_inst0_O};
endmodule

module main (input  CLK, input [1:0] I, output [1:0] O);
wire [1:0] reg_O;
Register2 reg (.I(I), .O(reg_O), .CLK(CLK));
assign O = reg_O;
endmodule

