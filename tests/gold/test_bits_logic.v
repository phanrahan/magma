module test_circuit (input [7:0] a, input [7:0] b, input [7:0] c, input [2:0] d, output [7:0] e);
wire [7:0] inst0_out;
wire [7:0] inst1_out;
wire [7:0] inst2_out;
wire [7:0] inst3_out;
wire [7:0] inst4_out;
wire [7:0] inst5_out;
wire [7:0] inst6_out;
wire [7:0] inst7_out;
coreir_and #(.WIDTH(8)) inst0 (.in0(a), .in1(b), .out(inst0_out));
coreir_not #(.WIDTH(8)) inst1 (.I(c), .out(inst1_out));
coreir_xor #(.WIDTH(8)) inst2 (.in0(b), .in1(inst1_out), .out(inst2_out));
coreir_lshr #(.SHIFTBITS(3), .WIDTH(8)) inst3 (.I(inst2_out), .out(inst3_out));
coreir_dlshr #(.WIDTH(8)) inst4 (.in0(inst3_out), .in1(d), .out(inst4_out));
coreir_shl #(.SHIFTBITS(3), .WIDTH(8)) inst5 (.I(inst4_out), .out(inst5_out));
coreir_dshl #(.WIDTH(8)) inst6 (.in0(inst5_out), .in1(d), .out(inst6_out));
coreir_or #(.WIDTH(8)) inst7 (.in0(inst0_out), .in1(inst6_out), .out(inst7_out));
assign e = inst7_out;
endmodule

