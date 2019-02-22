module ternary_nested2 (input [3:0] I, input [1:0] S, output  O);
wire  Mux2_inst0_O;
wire  Mux2_inst1_O;
Mux2 Mux2_inst0 (.I0(I[1]), .I1(I[0]), .S(S[0]), .O(Mux2_inst0_O));
Mux2 Mux2_inst1 (.I0(I[2]), .I1(Mux2_inst0_O), .S(S[1]), .O(Mux2_inst1_O));
assign O = Mux2_inst1_O;
endmodule

