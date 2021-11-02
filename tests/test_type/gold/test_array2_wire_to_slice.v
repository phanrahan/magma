module mantle_concatNArrT__Ns22__t_childBitIn (
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
wire [3:0] ConcatN_inst0_out;
mantle_concatNArrT__Ns22__t_childBitIn ConcatN_inst0 (
    .in0(I[3:2]),
    .in1(I[1:0]),
    .out(ConcatN_inst0_out)
);
assign O = ConcatN_inst0_out;
endmodule

