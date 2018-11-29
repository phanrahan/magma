module test_assign_operator_3_verilog (input [2:0] a, input [2:0] b, output [2:0] c);
wire [2:0] And3_inst0_O;
And3 And3_inst0 (.I0(a), .I1(b), .O(And3_inst0_O));
assign c = And3_inst0_O;
endmodule

