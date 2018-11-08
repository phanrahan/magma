module test_assign_operator2_3_verilog (input [2:0] a, input [2:0] b, output [2:0] c);
wire [2:0] inst0_O;
And3 inst0 (.I0(inst0_O), .I1(a), .O(inst0_O));
assign c = b;
endmodule

