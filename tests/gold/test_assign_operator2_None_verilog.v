module test_assign_operator2_None_verilog (input  a, input  b, output  c);
wire  AndNone_inst0_O;
AndNone AndNone_inst0 (.I0(AndNone_inst0_O), .I1(a), .O(AndNone_inst0_O));
assign c = b;
endmodule

