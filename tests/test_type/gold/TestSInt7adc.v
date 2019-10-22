module coreir_add #(parameter width = 1) (input [width-1:0] in0, input [width-1:0] in1, output [width-1:0] out);
  assign out = in0 + in1;
endmodule

module corebit_const #(parameter value = 1) (output out);
  assign out = value;
endmodule

module TestBinary (input CIN, output COUT, input [6:0] I0, input [6:0] I1, output [6:0] O);
wire bit_const_0_None_out;
wire [7:0] magma_Bits_8_add_inst0_out;
wire [7:0] magma_Bits_8_add_inst1_out;
corebit_const #(.value(0)) bit_const_0_None(.out(bit_const_0_None_out));
coreir_add #(.width(8)) magma_Bits_8_add_inst0(.in0({I0[6],I0[6],I0[5],I0[4],I0[3],I0[2],I0[1],I0[0]}), .in1({I1[6],I1[6],I1[5],I1[4],I1[3],I1[2],I1[1],I1[0]}), .out(magma_Bits_8_add_inst0_out));
coreir_add #(.width(8)) magma_Bits_8_add_inst1(.in0(magma_Bits_8_add_inst0_out), .in1({bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,CIN}), .out(magma_Bits_8_add_inst1_out));
assign COUT = magma_Bits_8_add_inst1_out[7];
assign O = {magma_Bits_8_add_inst1_out[6],magma_Bits_8_add_inst1_out[5],magma_Bits_8_add_inst1_out[4],magma_Bits_8_add_inst1_out[3],magma_Bits_8_add_inst1_out[2],magma_Bits_8_add_inst1_out[1],magma_Bits_8_add_inst1_out[0]};
endmodule

