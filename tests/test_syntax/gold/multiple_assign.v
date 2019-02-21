module eq (input  I0, input  I1, output  O);
assign O = 1'b0;
endmodule

module logic (input  a_0, output  O0);
wire  eq_inst0_O;
wire  Mux2_inst0_O;
eq eq_inst0 (.I0(a_0), .I1(1'b0), .O(eq_inst0_O));
Mux2 Mux2_inst0 (.I0(1'b1), .I1(1'b0), .S(eq_inst0_O), .O(Mux2_inst0_O));
assign O0 = Mux2_inst0_O;
endmodule

module Foo (input  a, output  c);
wire  logic_inst0_O0;
logic logic_inst0 (.a_0(a), .O0(logic_inst0_O0));
assign c = logic_inst0_O0;
endmodule

