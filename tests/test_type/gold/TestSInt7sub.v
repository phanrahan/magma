module coreir_sub #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 - in1;
endmodule

module TestBinary (
    input [6:0] I0,
    input [6:0] I1,
    output [6:0] O
);
wire [6:0] magma_SInt_7_sub_inst0_out;
coreir_sub #(
    .width(7)
) magma_SInt_7_sub_inst0 (
    .in0(I0),
    .in1(I1),
    .out(magma_SInt_7_sub_inst0_out)
);
assign O = magma_SInt_7_sub_inst0_out;
endmodule

