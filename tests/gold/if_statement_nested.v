module if_statement_nested (input [3:0] I, input [1:0] S, output  O);
wire  inst0_O;
wire  inst1_O;
wire  inst2_O;
Mux2 inst0 (.I0(I[0]), .I1(I[1]), .S(S[1]), .O(inst0_O));
Mux2 inst1 (.I0(I[2]), .I1(I[3]), .S(S[1]), .O(inst1_O));
Mux2 inst2 (.I0(inst0_O), .I1(inst1_O), .S(S[0]), .O(inst2_O));
assign O = inst2_O;
endmodule

