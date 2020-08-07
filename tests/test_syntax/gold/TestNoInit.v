module corebit_and (
    input in0,
    input in1,
    output out
);
  assign out = in0 & in1;
endmodule

module TestNoInit_comb (
    input a,
    input b,
    output O
);
wire magma_Bit_and_inst0_in0;
wire magma_Bit_and_inst0_in1;
wire magma_Bit_and_inst0_out;
assign magma_Bit_and_inst0_in0 = a;
assign magma_Bit_and_inst0_in1 = b;
corebit_and magma_Bit_and_inst0 (
    .in0(magma_Bit_and_inst0_in0),
    .in1(magma_Bit_and_inst0_in1),
    .out(magma_Bit_and_inst0_out)
);
assign O = magma_Bit_and_inst0_out;
endmodule

module TestNoInit (
    input a,
    input b,
    input CLK,
    input ASYNCRESET,
    output O
);
wire TestNoInit_comb_inst0_a;
wire TestNoInit_comb_inst0_b;
wire TestNoInit_comb_inst0_O;
assign TestNoInit_comb_inst0_a = a;
assign TestNoInit_comb_inst0_b = b;
TestNoInit_comb TestNoInit_comb_inst0 (
    .a(TestNoInit_comb_inst0_a),
    .b(TestNoInit_comb_inst0_b),
    .O(TestNoInit_comb_inst0_O)
);
assign O = TestNoInit_comb_inst0_O;
endmodule

