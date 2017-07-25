module test_circuit (input  a, input  b, input  c, output  d);
wire  inst0_O;
wire  inst1_O;
wire  inst2_O;
wire  inst3_O;
coreir_and #(.WIDTH(1)) inst0 (.I0(a), .I1(b), .O(inst0_O));
coreir_not #(.WIDTH(1)) inst1 (.I(c), .O(inst1_O));
coreir_xor #(.WIDTH(1)) inst2 (.I0(b), .I1(inst1_O), .O(inst2_O));
coreir_or #(.WIDTH(1)) inst3 (.I0(inst0_O), .I1(inst2_O), .O(inst3_O));
assign d = inst3_O;
endmodule

