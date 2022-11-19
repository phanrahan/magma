module test_assign_operator2_None_verilog (input  a, input  b, output  c);
wire  and2_O;
AndNone and2 (.I0(and2_O), .I1(a), .O(and2_O));
assign c = b;
endmodule

