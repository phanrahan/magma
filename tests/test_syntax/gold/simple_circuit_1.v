module eq (input  I0, input  I1, output  O);
assign O = 1'b0;
endmodule

module logic (input  a, output  O0);
wire  eq_inst0_O;
wire  Mux2xOutBit_inst0_O;
eq eq_inst0 (.I0(a), .I1(1'b0), .O(eq_inst0_O));
Mux2xOutBit Mux2xOutBit_inst0 (.I0(1'b0), .I1(1'b1), .S(eq_inst0_O), .O(Mux2xOutBit_inst0_O));
assign O0 = Mux2xOutBit_inst0_O;
endmodule

module Foo (input  a, output  c);
wire  logic_inst0_O0;
logic logic_inst0 (.a(a), .O0(logic_inst0_O0));
assign c = logic_inst0_O0;
endmodule

