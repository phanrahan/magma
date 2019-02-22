module basic_func (input [1:0] I, input  S, output  O);
assign O = I[1];
endmodule

module basic_function_call (input [1:0] I, input  S, output  O);
wire  basic_func_inst0_O;
basic_func basic_func_inst0 (.I(I), .S(S), .O(basic_func_inst0_O));
assign O = basic_func_inst0_O;
endmodule

