module basic_func (input [1:0] I_0, input  S_0, output  O);
assign O = I_0[1];
endmodule

module basic_function_call (input [1:0] I_0, input  S_0, output  O);
wire  basic_func_inst0_O;
basic_func basic_func_inst0 (.I_0(I_0), .S_0(S_0), .O(basic_func_inst0_O));
assign O = basic_func_inst0_O;
endmodule

