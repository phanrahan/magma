module ternary_nested (input [3:0] I, input [1:0] S, output  O);
wire  Mux2_inst0_O;
wire  Mux2_inst1_O;
Mux2 Mux2_inst0 (.I0(I[2]), .I1(I[1]), .S(S[1]), .O(Mux2_inst0_O));
Mux2 Mux2_inst1 (.I0(Mux2_inst0_O), .I1(I[0]), .S(S[0]), .O(Mux2_inst1_O));
assign O = Mux2_inst1_O;
endmodule

