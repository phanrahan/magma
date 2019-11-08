module corebit_not (input in, output out);
  assign out = ~in;
endmodule

module Foo_comb (output O, input a);
wire magma_Bit_not_inst0_out;
corebit_not magma_Bit_not_inst0(.in(a), .out(magma_Bit_not_inst0_out));
assign O = magma_Bit_not_inst0_out;
endmodule

module Foo (input ASYNCRESET, input CLK, output O, input a);
wire Foo_comb_inst0_O;
Foo_comb Foo_comb_inst0(.O(Foo_comb_inst0_O), .a(a));
assign O = Foo_comb_inst0_O;
endmodule

