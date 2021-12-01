module mantle_concatNArrT__Ns71__t_childBitIn (
    input [6:0] in0,
    input [0:0] in1,
    output [7:0] out
);
assign out = {in1[0],in0[6],in0[5],in0[4],in0[3],in0[2],in0[1],in0[0]};
endmodule

module mantle_concatNArrT__Ns17__t_childBitIn (
    input [0:0] in0,
    input [6:0] in1,
    output [7:0] out
);
assign out = {in1[6],in1[5],in1[4],in1[3],in1[2],in1[1],in1[0],in0[0]};
endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module TestBinary (
    input [6:0] I0,
    input [6:0] I1,
    input CIN,
    output [6:0] O,
    output COUT
);
wire [7:0] ConcatN_inst0_out;
wire [7:0] ConcatN_inst1_out;
wire [7:0] ConcatN_inst2_out;
wire [6:0] Const_inst0_out;
wire [7:0] magma_SInt_8_add_inst0_out;
wire [7:0] magma_SInt_8_add_inst1_out;
mantle_concatNArrT__Ns71__t_childBitIn ConcatN_inst0 (
    .in0(I0),
    .in1(I0[6]),
    .out(ConcatN_inst0_out)
);
mantle_concatNArrT__Ns71__t_childBitIn ConcatN_inst1 (
    .in0(I1),
    .in1(I1[6]),
    .out(ConcatN_inst1_out)
);
mantle_concatNArrT__Ns17__t_childBitIn ConcatN_inst2 (
    .in0(CIN),
    .in1(Const_inst0_out),
    .out(ConcatN_inst2_out)
);
coreir_const #(
    .value(7'h00),
    .width(7)
) Const_inst0 (
    .out(Const_inst0_out)
);
coreir_add #(
    .width(8)
) magma_SInt_8_add_inst0 (
    .in0(ConcatN_inst0_out),
    .in1(ConcatN_inst1_out),
    .out(magma_SInt_8_add_inst0_out)
);
coreir_add #(
    .width(8)
) magma_SInt_8_add_inst1 (
    .in0(magma_SInt_8_add_inst0_out),
    .in1(ConcatN_inst2_out),
    .out(magma_SInt_8_add_inst1_out)
);
assign O = magma_SInt_8_add_inst1_out[6:0];
assign COUT = magma_SInt_8_add_inst1_out[7];
endmodule

