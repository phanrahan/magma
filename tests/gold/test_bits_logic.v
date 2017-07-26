module test_circuit (input [3:0] a, input [3:0] b, input [3:0] c, output [3:0] d);
wire [3:0] inst0_out;
wire [3:0] inst1_out;
wire [3:0] inst2_out;
coreir_and #(.WIDTH(4)) inst0 (.in0(a), .in1(b), .out(inst0_out));
coreir_xor #(.WIDTH(4)) inst1 (.in0(b), .in1(c), .out(inst1_out));
coreir_or #(.WIDTH(4)) inst2 (.in0(inst0_out), .in1(inst1_out), .out(inst2_out));
assign d = inst2_out;
endmodule

