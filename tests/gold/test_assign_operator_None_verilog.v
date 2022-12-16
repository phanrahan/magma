module test_assign_operator_None_verilog (input  a, input  b, output  c);
wire  AndNone_inst0_O;
AndNone AndNone_inst0 (.I0(a), .I1(b), .O(AndNone_inst0_O));
assign c = AndNone_inst0_O;
endmodule

