module mantle_concatNArrT__Ns11__t_childBitIn (
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
wire [1:0] ConcatN_inst0_out;
mantle_concatNArrT__Ns11__t_childBitIn ConcatN_inst0 (
    .in0(I[1:1]),
    .in1(I[0:0]),
    .out(ConcatN_inst0_out)
);
assign O = ConcatN_inst0_out;
endmodule

