module coreir_mux #(parameter width = 1) (input [width-1:0] in0, input [width-1:0] in1, input sel, output [width-1:0] out);
  assign out = sel ? in1 : in0;
endmodule

module A_comb (output [0:0] O, input a, input [1:0] b);
wire [0:0] magma_Bit_ite_Out_Bits_1_inst0_out;
coreir_mux #(.width(1)) magma_Bit_ite_Out_Bits_1_inst0(.in0(b[0]), .in1(a), .out(magma_Bit_ite_Out_Bits_1_inst0_out), .sel(a));
assign O = magma_Bit_ite_Out_Bits_1_inst0_out;
endmodule

module A (input ASYNCRESET, input CLK, output [0:0] O, input a, input [1:0] b);
wire [0:0] A_comb_inst0_O;
A_comb A_comb_inst0(.O(A_comb_inst0_O), .a(a), .b(b));
assign O = A_comb_inst0_O;
endmodule

