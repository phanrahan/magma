module corebit_mux (input in0, input in1, input sel, output out);
  assign out = sel ? in1 : in0;
endmodule

module TestITE (input I0, input I1, input S, output O);
wire magma_Bit_ite_Out_Bit_inst0_out;
corebit_mux magma_Bit_ite_Out_Bit_inst0(.in0(I1), .in1(I0), .sel(S), .out(magma_Bit_ite_Out_Bit_inst0_out));
assign O = magma_Bit_ite_Out_Bit_inst0_out;
endmodule

