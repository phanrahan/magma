module eq2 (input [1:0] I0, input [1:0] I1, output  O);
assign O = 1'b0;
endmodule

module logic (input [1:0] a, output [1:0] O0, output [1:0] O1);
wire  eq2_inst0_O;
wire [1:0] Mux2_x2_inst0_O;
wire  eq2_inst1_O;
wire [1:0] Mux2_x2_inst1_O;
eq2 eq2_inst0 (.I0(a), .I1({1'b0,1'b0}), .O(eq2_inst0_O));
Mux2_x2 Mux2_x2_inst0 (.I0({1'b1,1'b0}), .I1({1'b0,1'b1}), .S(eq2_inst0_O), .O(Mux2_x2_inst0_O));
eq2 eq2_inst1 (.I0(a), .I1({1'b0,1'b0}), .O(eq2_inst1_O));
Mux2_x2 Mux2_x2_inst1 (.I0({1'b1,1'b1}), .I1({1'b0,1'b0}), .S(eq2_inst1_O), .O(Mux2_x2_inst1_O));
assign O0 = Mux2_x2_inst0_O;
assign O1 = Mux2_x2_inst1_O;
endmodule

module Foo (input [1:0] a, output [1:0] c, output [1:0] d);
wire [1:0] logic_inst0_O0;
wire [1:0] logic_inst0_O1;
logic logic_inst0 (.a(a), .O0(logic_inst0_O0), .O1(logic_inst0_O1));
assign c = logic_inst0_O0;
assign d = logic_inst0_O1;
endmodule

