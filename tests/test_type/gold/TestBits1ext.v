module mantle_concatNArrT__Ns13__t_childBitIn (
    input [0:0] in0,
    input [2:0] in1,
    output [3:0] out
);
assign out = {in1[2],in1[1],in1[0],in0[0]};
endmodule

module coreir_term #(
    parameter width = 1
) (
    input [width-1:0] in
);

endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module TestExt (
    input [0:0] I,
    output [3:0] O
);
wire [3:0] ConcatN_inst0_out;
wire [2:0] Const_inst0_out;
mantle_concatNArrT__Ns13__t_childBitIn ConcatN_inst0 (
    .in0(I),
    .in1(Const_inst0_out),
    .out(ConcatN_inst0_out)
);
coreir_const #(
    .value(3'h0),
    .width(3)
) Const_inst0 (
    .out(Const_inst0_out)
);
coreir_term #(
    .width(3)
) term_inst0 (
    .in(Const_inst0_out)
);
assign O = ConcatN_inst0_out;
endmodule

