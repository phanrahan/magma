module ternary_nested2 (input [3:0] I_0, input [1:0] S_0, output  O);
wire  Mux2_inst0_O;
wire  Mux2_inst1_O;
Mux2 Mux2_inst0 (.I0(I_0[1]), .I1(I_0[0]), .S(S_0[0]), .O(Mux2_inst0_O));
Mux2 Mux2_inst1 (.I0(I_0[2]), .I1(Mux2_inst0_O), .S(S_0[1]), .O(Mux2_inst1_O));
assign O = Mux2_inst1_O;
endmodule

