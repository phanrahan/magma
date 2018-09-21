module Not (input  I, output  O);
assign O = 1'b0;
endmodule

module logic (input [9:0] a, output [9:0] O);
wire  inst0_O;
wire  inst1_O;
wire  inst2_O;
wire  inst3_O;
wire  inst4_O;
wire  inst5_O;
wire  inst6_O;
wire  inst7_O;
wire  inst8_O;
wire  inst9_O;
Not inst0 (.I(a[0]), .O(inst0_O));
Not inst1 (.I(a[1]), .O(inst1_O));
Not inst2 (.I(a[2]), .O(inst2_O));
Not inst3 (.I(a[3]), .O(inst3_O));
Not inst4 (.I(a[4]), .O(inst4_O));
Not inst5 (.I(a[5]), .O(inst5_O));
Not inst6 (.I(a[6]), .O(inst6_O));
Not inst7 (.I(a[7]), .O(inst7_O));
Not inst8 (.I(a[8]), .O(inst8_O));
Not inst9 (.I(a[9]), .O(inst9_O));
assign O = {inst9_O,inst8_O,inst7_O,inst6_O,inst5_O,inst4_O,inst3_O,inst2_O,inst1_O,inst0_O};
endmodule

module Foo (input [9:0] a, output [9:0] c);
wire [9:0] inst0_O;
logic inst0 (.a(a), .O(inst0_O));
assign c = inst0_O;
endmodule

