module ternary (input [1:0] I, input  S, output  O);
wire  Mux2_inst0_O;
Mux2 Mux2_inst0 (.I0(I[1]), .I1(I[0]), .S(S), .O(Mux2_inst0_O));
assign O = Mux2_inst0_O;
endmodule

