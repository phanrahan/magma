module test_circuit (input [7:0] a, input [7:0] b, input [7:0] c, input [2:0] d, output [7:0] e);
wire [7:0] inst0_O;
wire [7:0] inst1_O;
wire [7:0] inst2_O;
wire [7:0] inst3_O;
wire [7:0] inst4_O;
wire [7:0] inst5_O;
wire [7:0] inst6_O;
wire [7:0] inst7_O;
coreir_and #(.WIDTH(8)) inst0 (.I0(a), .I1(b), .O(inst0_O));
coreir_not #(.WIDTH(8)) inst1 (.I(c), .O(inst1_O));
coreir_xor #(.WIDTH(8)) inst2 (.I0(b), .I1(inst1_O), .O(inst2_O));
coreir_lshr #(.SHIFTBITS(3), .WIDTH(8)) inst3 (.I(inst2_O), .O(inst3_O));
coreir_dlshr #(.WIDTH(8)) inst4 (.I0(inst3_O), .I1(d), .O(inst4_O));
coreir_shl #(.SHIFTBITS(3), .WIDTH(8)) inst5 (.I(inst4_O), .O(inst5_O));
coreir_dshl #(.WIDTH(8)) inst6 (.I0(inst5_O), .I1(d), .O(inst6_O));
coreir_or #(.WIDTH(8)) inst7 (.I0(inst0_O), .I1(inst6_O), .O(inst7_O));
assign e = inst7_O;
endmodule

