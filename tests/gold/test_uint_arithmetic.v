module test_circuit (input [7:0] in0, input [7:0] in1, output  out);
wire [7:0] inst0_out;
wire [7:0] inst1_out;
wire [7:0] inst2_out;
wire [7:0] inst3_out;
wire  inst4_out;
wire [7:0] inst5_out;
wire  inst6_out;
wire [7:0] inst7_out;
wire  inst8_out;
wire [7:0] inst9_out;
wire  inst10_out;
coreir_add #(.WIDTH(8)) inst0 (.in0(in0), .in1(in1), .out(inst0_out));
coreir_sub #(.WIDTH(8)) inst1 (.in0(inst0_out), .in1(in1), .out(inst1_out));
coreir_mul #(.WIDTH(8)) inst2 (.in0(inst0_out), .in1(in0), .out(inst2_out));
coreir_div #(.WIDTH(8)) inst3 (.in0(inst1_out), .in1(inst2_out), .out(inst3_out));
coreir_ugt #(.WIDTH(8)) inst4 (.in0(inst3_out), .in1(in0), .out(inst4_out));
coreir_mul #(.WIDTH(8)) inst5 (.in0(inst1_out), .in1(inst2_out), .out(inst5_out));
coreir_ult #(.WIDTH(8)) inst6 (.in0(inst5_out), .in1({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b1}), .out(inst6_out));
coreir_sub #(.WIDTH(8)) inst7 (.in0(inst0_out), .in1(inst2_out), .out(inst7_out));
coreir_uge #(.WIDTH(8)) inst8 (.in0(inst7_out), .in1(in0), .out(inst8_out));
coreir_add #(.WIDTH(8)) inst9 (.in0(inst1_out), .in1(inst2_out), .out(inst9_out));
coreir_ule #(.WIDTH(8)) inst10 (.in0(inst9_out), .in1({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b1}), .out(inst10_out));
assign out = inst10_out;
endmodule

