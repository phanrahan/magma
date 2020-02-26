module corebit_const #(parameter value = 1) (output out);
  assign out = value;
endmodule

module TestProductReplace_comb (output O_x, output O_y);
wire bit_const_1_None_out;
corebit_const #(.value(1'b1)) bit_const_1_None(.out(bit_const_1_None_out));
assign O_x = bit_const_1_None_out;
assign O_y = bit_const_1_None_out;
endmodule

module TestProductReplace (input CLK, output O_x, output O_y);
wire TestProductReplace_comb_inst0_O_x;
wire TestProductReplace_comb_inst0_O_y;
TestProductReplace_comb TestProductReplace_comb_inst0(.O_x(TestProductReplace_comb_inst0_O_x), .O_y(TestProductReplace_comb_inst0_O_y));
assign O_x = TestProductReplace_comb_inst0_O_x;
assign O_y = TestProductReplace_comb_inst0_O_y;
endmodule

