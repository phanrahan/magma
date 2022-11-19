module test_assign_operator2_3_verilog (input [2:0] a, input [2:0] b, output [2:0] c);
wire [2:0] and2_O;
And3 and2 (.I0(and2_O), .I1(a), .O(and2_O));
assign c = b;
endmodule

