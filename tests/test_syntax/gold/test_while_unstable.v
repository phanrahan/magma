module f (input [3:0] a, input [3:0] b, output [3:0] O0, output [3:0] O1);
wire [3:0] coreir_add4_inst0_out;
wire [3:0] coreir_add4_inst1_out;
coreir_add4 coreir_add4_inst0 (.I0(a), .I1({1'b0,1'b0,1'b0,1'b1}), .O(coreir_add4_inst0_out));
coreir_add4 coreir_add4_inst1 (.I0(b), .I1({1'b0,1'b0,1'b1,1'b0}), .O(coreir_add4_inst1_out));
assign O0 = coreir_add4_inst0_out;
assign O1 = coreir_add4_inst1_out;
endmodule

module g (input [3:0] c, output [3:0] O);
wire [3:0] f_inst0_O0;
wire [3:0] f_inst0_O1;
f f_inst0 (.a(c), .b(f_inst0_O0), .O0(f_inst0_O0), .O1(f_inst0_O1));
assign O = f_inst0_O1;
endmodule

