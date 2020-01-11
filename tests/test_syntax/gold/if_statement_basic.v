module basic_if (input [1:0] I, input  S, output  O);
wire  Mux2xOutBit_inst0_O;
Mux2xOutBit Mux2xOutBit_inst0 (.I0(I[1]), .I1(I[0]), .S(S), .O(Mux2xOutBit_inst0_O));
assign O = Mux2xOutBit_inst0_O;
endmodule

