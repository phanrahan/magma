module mantle_wire__typeBit2 (
    input [1:0] in,
    output [1:0] out
);
assign out = in;
endmodule

module mantle_sliceArrT__hi4__lo2__tBitIn4 (
    input [3:0] in,
    output [1:0] out
);
assign out = {in[3],in[2]};
endmodule

module mantle_sliceArrT__hi2__lo0__tBitIn4 (
    input [3:0] in,
    output [1:0] out
);
assign out = {in[1],in[0]};
endmodule

module mantle_concatArrT__t0BitIn2__t1BitIn2 (
    input [1:0] in0,
    input [1:0] in1,
    output [3:0] out
);
assign out = {in1[1],in1[0],in0[1],in0[0]};
endmodule

module Foo (
    input [3:0] I,
    output [3:0] O
);
wire [3:0] Concat_inst0_out;
wire [1:0] Slice_inst0_out;
wire [1:0] Slice_inst1_out;
wire [1:0] Wire_inst0_out;
wire [1:0] Wire_inst1_out;
mantle_concatArrT__t0BitIn2__t1BitIn2 Concat_inst0 (
    .in0(Wire_inst0_out),
    .in1(Wire_inst1_out),
    .out(Concat_inst0_out)
);
mantle_sliceArrT__hi4__lo2__tBitIn4 Slice_inst0 (
    .in(I),
    .out(Slice_inst0_out)
);
mantle_sliceArrT__hi2__lo0__tBitIn4 Slice_inst1 (
    .in(I),
    .out(Slice_inst1_out)
);
mantle_wire__typeBit2 Wire_inst0 (
    .in(Slice_inst0_out),
    .out(Wire_inst0_out)
);
mantle_wire__typeBit2 Wire_inst1 (
    .in(Slice_inst1_out),
    .out(Wire_inst1_out)
);
assign O = Concat_inst0_out;
endmodule

