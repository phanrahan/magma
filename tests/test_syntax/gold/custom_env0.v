module basic_fun (input  I, input  S, output  O);
wire  Mux2_inst0_O;
Mux2 Mux2_inst0 (.I0(1'b0), .I1(I), .S(S), .O(Mux2_inst0_O));
assign O = Mux2_inst0_O;
endmodule

