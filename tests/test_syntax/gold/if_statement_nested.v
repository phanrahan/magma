module Not (input  I, output  O);
assign O = 1'b0;
endmodule

module if_statement_nested (input [3:0] I, input [1:0] S, output  O);
wire  Mux2_inst0_O;
wire  Not_inst0_O;
wire  Mux2_inst1_O;
wire  Mux2_inst2_O;
Mux2 Mux2_inst0 (.I0(I[1]), .I1(I[0]), .S(S[1]), .O(Mux2_inst0_O));
Not Not_inst0 (.I(S[1]), .O(Not_inst0_O));
Mux2 Mux2_inst1 (.I0(I[2]), .I1(Mux2_inst0_O), .S(Not_inst0_O), .O(Mux2_inst1_O));
Mux2 Mux2_inst2 (.I0(I[3]), .I1(Mux2_inst1_O), .S(S[1]), .O(Mux2_inst2_O));
assign O = Mux2_inst2_O;
endmodule

