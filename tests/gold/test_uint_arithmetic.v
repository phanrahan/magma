module test_circuit (input [7:0] in0, input [7:0] in1, output  out);
wire [7:0] inst0_O;
wire [7:0] inst1_O;
wire [7:0] inst2_O;
wire [7:0] inst3_O;
wire  inst4_O;
wire [7:0] inst5_O;
wire  inst6_O;
wire [7:0] inst7_O;
wire  inst8_O;
wire [7:0] inst9_O;
wire  inst10_O;
coreir_add #(.WIDTH(8)) inst0 (.I0(in0), .I1(in1), .O(inst0_O));
coreir_sub #(.WIDTH(8)) inst1 (.I0(inst0_O), .I1(in1), .O(inst1_O));
coreir_mul #(.WIDTH(8)) inst2 (.I0(inst0_O), .I1(in0), .O(inst2_O));
coreir_div #(.WIDTH(8)) inst3 (.I0(inst1_O), .I1(inst2_O), .O(inst3_O));
coreir_ugt #(.WIDTH(8)) inst4 (.I0(inst3_O), .I1(in0), .O(inst4_O));
coreir_mul #(.WIDTH(8)) inst5 (.I0(inst1_O), .I1(inst2_O), .O(inst5_O));
coreir_ult #(.WIDTH(8)) inst6 (.I0(inst5_O), .I1({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b1}), .O(inst6_O));
coreir_sub #(.WIDTH(8)) inst7 (.I0(inst0_O), .I1(inst2_O), .O(inst7_O));
coreir_uge #(.WIDTH(8)) inst8 (.I0(inst7_O), .I1(in0), .O(inst8_O));
coreir_add #(.WIDTH(8)) inst9 (.I0(inst1_O), .I1(inst2_O), .O(inst9_O));
coreir_ule #(.WIDTH(8)) inst10 (.I0(inst9_O), .I1({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b1}), .O(inst10_O));
assign out = inst10_O;
endmodule

