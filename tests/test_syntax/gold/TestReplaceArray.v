module coreir_const #(parameter width = 1, parameter value = 1) (output [width-1:0] out);
  assign out = value;
endmodule

module TestReplaceArray_comb (output [1:0] O);
wire [1:0] const_3_2_out;
coreir_const #(.value(2'h3), .width(2)) const_3_2(.out(const_3_2_out));
assign O = const_3_2_out;
endmodule

module TestReplaceArray (input CLK, output [1:0] O);
wire [1:0] TestReplaceArray_comb_inst0_O;
TestReplaceArray_comb TestReplaceArray_comb_inst0(.O(TestReplaceArray_comb_inst0_O));
assign O = TestReplaceArray_comb_inst0_O;
endmodule

