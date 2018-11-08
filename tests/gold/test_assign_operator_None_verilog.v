module test_assign_operator_None_verilog (input  a, input  b, output  c);
wire  inst0_O;
AndNone inst0 (.I0(a), .I1(b), .O(inst0_O));
assign c = inst0_O;
endmodule

