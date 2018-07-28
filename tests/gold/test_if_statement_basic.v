module TestIfStatementBasic (input [1:0] I, input  S, output  O);
wire  inst0_O;
Mux2 inst0 (.I0(I[0]), .I1(I[1]), .S(S), .O(inst0_O));
assign O = inst0_O;
endmodule

