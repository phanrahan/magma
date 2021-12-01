module mantle_concatNArrT__Ns31__t_childBitIn (
    input [2:0] in0,
    input [0:0] in1,
    output [3:0] out
);
assign out = {in1[0],in0[2],in0[1],in0[0]};
endmodule

module mantle_concatNArrT__Ns13__t_childBitIn (
    input [0:0] in0,
    input [2:0] in1,
    output [3:0] out
);
assign out = {in1[2],in1[1],in1[0],in0[0]};
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
    input [2:0] I0,
    input [2:0] I1,
    input CIN,
    output [2:0] O,
    output COUT
);
wire [3:0] ConcatN_inst0_out;
wire [3:0] ConcatN_inst1_out;
wire [3:0] ConcatN_inst2_out;
wire [0:0] Const_inst0_out;
wire [0:0] Const_inst1_out;
wire [2:0] Const_inst2_out;
wire [3:0] magma_UInt_4_add_inst0_out;
wire [3:0] magma_UInt_4_add_inst1_out;
mantle_concatNArrT__Ns31__t_childBitIn ConcatN_inst0 (
    .in0(I0),
    .in1(Const_inst0_out),
    .out(ConcatN_inst0_out)
);
mantle_concatNArrT__Ns31__t_childBitIn ConcatN_inst1 (
    .in0(I1),
    .in1(Const_inst1_out),
    .out(ConcatN_inst1_out)
);
mantle_concatNArrT__Ns13__t_childBitIn ConcatN_inst2 (
    .in0(CIN),
    .in1(Const_inst2_out),
    .out(ConcatN_inst2_out)
);
coreir_const #(
    .value(1'h0),
    .width(1)
) Const_inst0 (
    .out(Const_inst0_out)
);
coreir_const #(
    .value(1'h0),
    .width(1)
) Const_inst1 (
    .out(Const_inst1_out)
);
coreir_const #(
    .value(3'h0),
    .width(3)
) Const_inst2 (
    .out(Const_inst2_out)
);
coreir_add #(
    .width(4)
) magma_UInt_4_add_inst0 (
    .in0(ConcatN_inst0_out),
    .in1(ConcatN_inst1_out),
    .out(magma_UInt_4_add_inst0_out)
);
coreir_add #(
    .width(4)
) magma_UInt_4_add_inst1 (
    .in0(magma_UInt_4_add_inst0_out),
    .in1(ConcatN_inst2_out),
    .out(magma_UInt_4_add_inst1_out)
);
assign O = magma_UInt_4_add_inst1_out[2:0];
assign COUT = magma_UInt_4_add_inst1_out[3];
endmodule

