module coreir_mux #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    input sel,
    output [width-1:0] out
);
  assign out = sel ? in1 : in0;
endmodule

module A_comb (
    input a,
    input [1:0] b,
    output [0:0] O
);
wire [0:0] magma_Bit_ite_Out_Bits_1_inst0_out;
coreir_mux #(
    .width(1)
) magma_Bit_ite_Out_Bits_1_inst0 (
    .in0(b[0]),
    .in1(a),
    .sel(a),
    .out(magma_Bit_ite_Out_Bits_1_inst0_out)
);
assign O = magma_Bit_ite_Out_Bits_1_inst0_out;
endmodule

module A (
    input a,
    input [1:0] b,
    input CLK,
    input ASYNCRESET,
    output [0:0] O
);
wire [0:0] A_comb_inst0_O;
A_comb A_comb_inst0 (
    .a(a),
    .b(b),
    .O(A_comb_inst0_O)
);
assign O = A_comb_inst0_O;
endmodule

