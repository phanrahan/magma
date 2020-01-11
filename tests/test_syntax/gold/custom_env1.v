module basic_fun (input  I, input  S, output  O);
wire  Mux2xOutDigital_inst0_O;
Mux2xOutDigital Mux2xOutDigital_inst0 (.I0(1'b1), .I1(I), .S(S), .O(Mux2xOutDigital_inst0_O));
assign O = Mux2xOutDigital_inst0_O;
endmodule

