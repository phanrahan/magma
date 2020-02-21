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
wire magma_Bit_and_inst0_out;
corebit_and magma_Bit_and_inst0 (
    .in0(a),
    .in1(b),
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
wire TestNoInit_comb_inst0_O;
TestNoInit_comb TestNoInit_comb_inst0 (
    .a(a),
    .b(b),
    .O(TestNoInit_comb_inst0_O)
);
assign O = TestNoInit_comb_inst0_O;
endmodule

