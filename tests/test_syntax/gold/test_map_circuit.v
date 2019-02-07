module Not (input  I, output  O);
assign O = 1'b0;
endmodule

module logic (input [9:0] a_0, output [9:0] O);
wire  Not_inst0_O;
wire  Not_inst1_O;
wire  Not_inst2_O;
wire  Not_inst3_O;
wire  Not_inst4_O;
wire  Not_inst5_O;
wire  Not_inst6_O;
wire  Not_inst7_O;
wire  Not_inst8_O;
wire  Not_inst9_O;
Not Not_inst0 (.I(a_0[0]), .O(Not_inst0_O));
Not Not_inst1 (.I(a_0[1]), .O(Not_inst1_O));
Not Not_inst2 (.I(a_0[2]), .O(Not_inst2_O));
Not Not_inst3 (.I(a_0[3]), .O(Not_inst3_O));
Not Not_inst4 (.I(a_0[4]), .O(Not_inst4_O));
Not Not_inst5 (.I(a_0[5]), .O(Not_inst5_O));
Not Not_inst6 (.I(a_0[6]), .O(Not_inst6_O));
Not Not_inst7 (.I(a_0[7]), .O(Not_inst7_O));
Not Not_inst8 (.I(a_0[8]), .O(Not_inst8_O));
Not Not_inst9 (.I(a_0[9]), .O(Not_inst9_O));
assign O = {Not_inst9_O,Not_inst8_O,Not_inst7_O,Not_inst6_O,Not_inst5_O,Not_inst4_O,Not_inst3_O,Not_inst2_O,Not_inst1_O,Not_inst0_O};
endmodule

module Foo (input [9:0] a, output [9:0] c);
wire [9:0] logic_inst0_O;
logic logic_inst0 (.a_0(a), .O(logic_inst0_O));
assign c = logic_inst0_O;
endmodule

