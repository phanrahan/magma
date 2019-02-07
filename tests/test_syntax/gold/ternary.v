module ternary (input [1:0] I_0, input  S_0, output  O);
wire  Mux2_inst0_O;
Mux2 Mux2_inst0 (.I0(I_0[1]), .I1(I_0[0]), .S(S_0), .O(Mux2_inst0_O));
assign O = Mux2_inst0_O;
endmodule

