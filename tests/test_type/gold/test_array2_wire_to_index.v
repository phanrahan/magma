module mantle_getArrT__i1__tBitIn2 (
    input [1:0] in,
    output out
);
assign out = in[1];
endmodule

module mantle_getArrT__i0__tBitIn2 (
    input [1:0] in,
    output out
);
assign out = in[0];
endmodule

module mantle_concatArrT__t0BitIn1__t1BitIn1 (
    input [0:0] in0,
    input [0:0] in1,
    output [1:0] out
);
assign out = {in1[0],in0[0]};
endmodule

module Foo (
    input [1:0] I,
    output [1:0] O
);
wire [1:0] Concat_inst0_out;
wire Index_inst0_out;
wire Index_inst1_out;
mantle_concatArrT__t0BitIn1__t1BitIn1 Concat_inst0 (
    .in0(Index_inst0_out),
    .in1(Index_inst1_out),
    .out(Concat_inst0_out)
);
mantle_getArrT__i1__tBitIn2 Index_inst0 (
    .in(I),
    .out(Index_inst0_out)
);
mantle_getArrT__i0__tBitIn2 Index_inst1 (
    .in(I),
    .out(Index_inst1_out)
);
assign O = Concat_inst0_out;
endmodule

