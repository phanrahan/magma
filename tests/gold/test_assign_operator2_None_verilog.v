module test_assign_operator2_None_verilog (input  a, input  b, output  c);
wire  inst0_O;
AndNone inst0 (.I0(inst0_O), .I1(a), .O(inst0_O));
assign c = b;
endmodule

