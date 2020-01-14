module basic_fun (input  I, input  S, output  O);
wire  Mux2xOutBit_inst0_O;
Mux2xOutBit Mux2xOutBit_inst0 (.I0(1'b0), .I1(I), .S(S), .O(Mux2xOutBit_inst0_O));
assign O = Mux2xOutBit_inst0_O;
endmodule

