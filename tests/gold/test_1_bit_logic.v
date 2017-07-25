module test_circuit (input  a, input  b, input  c, output  d);
wire  inst0_out;
wire  inst1_out;
wire  inst2_out;
coreir_and #(.WIDTH(1)) inst0 (.in0(a), .in1(b), .out(inst0_out));
coreir_xor #(.WIDTH(1)) inst1 (.in0(b), .in1(c), .out(inst1_out));
coreir_or #(.WIDTH(1)) inst2 (.in0(inst0_out), .in1(inst1_out), .out(inst2_out));
assign d = inst2_out;
endmodule

