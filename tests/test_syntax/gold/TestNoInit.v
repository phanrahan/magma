module corebit_and (input in0, input in1, output out);
  assign out = in0 & in1;
endmodule

module TestNoInit_comb (output O, input a, input b);
wire magma_Bit_and_inst0_out;
corebit_and magma_Bit_and_inst0(.in0(a), .in1(b), .out(magma_Bit_and_inst0_out));
assign O = magma_Bit_and_inst0_out;
endmodule

module TestNoInit (input ASYNCRESET, input CLK, output O, input a, input b);
wire TestNoInit_comb_inst0_O;
TestNoInit_comb TestNoInit_comb_inst0(.O(TestNoInit_comb_inst0_O), .a(a), .b(b));
assign O = TestNoInit_comb_inst0_O;
endmodule

