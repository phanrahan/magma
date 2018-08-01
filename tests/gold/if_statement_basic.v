module basic_if (input [1:0] I, input  S, output  O);
wire  inst0_O;
Mux2 inst0 (.I0(I[1]), .I1(I[0]), .S(S), .O(inst0_O));
assign O = inst0_O;
endmodule

