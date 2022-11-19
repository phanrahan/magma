module test_assign_operator_None_verilog (input  a, input  b, output  c);
wire  and2_O;
AndNone and2 (.I0(a), .I1(b), .O(and2_O));
assign c = and2_O;
endmodule

