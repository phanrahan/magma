module mantle_wire__typeBit1 (
    input [0:0] in,
    output [0:0] out
);
assign out = in;
endmodule

module mantle_wire__typeBit (
    input in,
    output out
);
assign out = in;
endmodule

module mantle_liftArrT__tBit1 (
    input in,
    output [0:0] out
);
assign out = in;
endmodule

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
    input I__0,
    input [1:0] I__1,
    output O__0,
    output [1:0] O__1
);
wire [1:0] Concat_inst0_out;
wire Index_inst0_out;
wire Index_inst1_out;
wire [0:0] Lift_inst0_out;
wire [0:0] Lift_inst1_out;
wire [0:0] Wire_inst0_out;
wire Wire_inst1_out;
wire Wire_inst2_out;
mantle_concatArrT__t0BitIn1__t1BitIn1 Concat_inst0 (
    .in0(Wire_inst0_out),
    .in1(Lift_inst0_out),
    .out(Concat_inst0_out)
);
mantle_getArrT__i0__tBitIn2 Index_inst0 (
    .in(I__1),
    .out(Index_inst0_out)
);
mantle_getArrT__i1__tBitIn2 Index_inst1 (
    .in(I__1),
    .out(Index_inst1_out)
);
mantle_liftArrT__tBit1 Lift_inst0 (
    .in(Wire_inst1_out),
    .out(Lift_inst0_out)
);
mantle_liftArrT__tBit1 Lift_inst1 (
    .in(Wire_inst2_out),
    .out(Lift_inst1_out)
);
mantle_wire__typeBit1 Wire_inst0 (
    .in(Lift_inst1_out),
    .out(Wire_inst0_out)
);
mantle_wire__typeBit Wire_inst1 (
    .in(Index_inst0_out),
    .out(Wire_inst1_out)
);
mantle_wire__typeBit Wire_inst2 (
    .in(Index_inst1_out),
    .out(Wire_inst2_out)
);
assign O__0 = I__0;
assign O__1 = Concat_inst0_out;
endmodule

