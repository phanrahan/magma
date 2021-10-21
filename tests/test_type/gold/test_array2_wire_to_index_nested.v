module mantle_liftArrT__tBit21 (
    input [1:0] in,
    output [1:0] out [0:0]
);
assign out[0] = in;
endmodule

module mantle_getArrT__i1__tBitIn22 (
    input [1:0] in [1:0],
    output [1:0] out
);
assign out = in[1];
endmodule

module mantle_getArrT__i0__tBitIn22 (
    input [1:0] in [1:0],
    output [1:0] out
);
assign out = in[0];
endmodule

module mantle_concatArrT__t0BitIn21__t1BitIn21 (
    input [1:0] in0 [0:0],
    input [1:0] in1 [0:0],
    output [1:0] out [1:0]
);
assign out[1] = in1[0];
assign out[0] = in0[0];
endmodule

module Foo (
    input [1:0] I [1:0],
    output [1:0] O [1:0]
);
wire [1:0] Concat_inst0_out [1:0];
wire [1:0] Index_inst0_out;
wire [1:0] Index_inst1_out;
wire [1:0] Lift_inst0_out [0:0];
wire [1:0] Lift_inst1_out [0:0];
wire [1:0] Concat_inst0_in0 [0:0];
assign Concat_inst0_in0[0] = Lift_inst0_out[0];
wire [1:0] Concat_inst0_in1 [0:0];
assign Concat_inst0_in1[0] = Lift_inst1_out[0];
mantle_concatArrT__t0BitIn21__t1BitIn21 Concat_inst0 (
    .in0(Concat_inst0_in0),
    .in1(Concat_inst0_in1),
    .out(Concat_inst0_out)
);
wire [1:0] Index_inst0_in [1:0];
assign Index_inst0_in[1] = I[1];
assign Index_inst0_in[0] = I[0];
mantle_getArrT__i1__tBitIn22 Index_inst0 (
    .in(Index_inst0_in),
    .out(Index_inst0_out)
);
wire [1:0] Index_inst1_in [1:0];
assign Index_inst1_in[1] = I[1];
assign Index_inst1_in[0] = I[0];
mantle_getArrT__i0__tBitIn22 Index_inst1 (
    .in(Index_inst1_in),
    .out(Index_inst1_out)
);
mantle_liftArrT__tBit21 Lift_inst0 (
    .in(Index_inst0_out),
    .out(Lift_inst0_out)
);
mantle_liftArrT__tBit21 Lift_inst1 (
    .in(Index_inst1_out),
    .out(Lift_inst1_out)
);
assign O[1] = Concat_inst0_out[1];
assign O[0] = Concat_inst0_out[0];
endmodule

