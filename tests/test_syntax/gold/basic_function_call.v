module basic_func (input [1:0] I, input  S, output  O);
wire  Mux2xOutBit_inst0_O;
Mux2xOutBit Mux2xOutBit_inst0 (.I0(I[1]), .I1(I[0]), .S(S), .O(Mux2xOutBit_inst0_O));
assign O = Mux2xOutBit_inst0_O;
endmodule

module basic_function_call (input [1:0] I, input  S, output  O);
wire  basic_func_inst0_O;
basic_func basic_func_inst0 (.I(I), .S(S), .O(basic_func_inst0_O));
assign O = basic_func_inst0_O;
endmodule

