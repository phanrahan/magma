module coreir_add #(parameter width = 1) (input [width-1:0] in0, input [width-1:0] in1, output [width-1:0] out);
  assign out = in0 + in1;
endmodule

module corebit_const #(parameter value = 1) (output out);
  assign out = value;
endmodule

module TestBinary (input CIN, output COUT, input [0:0] I0, input [0:0] I1, output [0:0] O);
wire bit_const_0_None_out;
wire [1:0] magma_Bits_2_add_inst0_out;
wire [1:0] magma_Bits_2_add_inst1_out;
corebit_const #(.value(1'b0)) bit_const_0_None(.out(bit_const_0_None_out));
coreir_add #(.width(2)) magma_Bits_2_add_inst0(.in0({bit_const_0_None_out,I0[0]}), .in1({bit_const_0_None_out,I1[0]}), .out(magma_Bits_2_add_inst0_out));
coreir_add #(.width(2)) magma_Bits_2_add_inst1(.in0(magma_Bits_2_add_inst0_out), .in1({bit_const_0_None_out,CIN}), .out(magma_Bits_2_add_inst1_out));
assign COUT = magma_Bits_2_add_inst1_out[1];
assign O = magma_Bits_2_add_inst1_out[0];
endmodule

