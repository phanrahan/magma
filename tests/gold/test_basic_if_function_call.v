module basic_if (input [1:0] I, input  S, output  O);
wire  inst0_O;
Mux2 inst0 (.I0(I[0]), .I1(I[1]), .S(S), .O(inst0_O));
assign O = inst0_O;
endmodule

module test_basic_if_function_call (input [1:0] I, input  S, output  O);
wire  inst0_O;
basic_if inst0 (.I(I), .S(S), .O(inst0_O));
assign O = inst0_O;
endmodule

