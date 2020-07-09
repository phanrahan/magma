module mantle_wire__typeBitIn5 (
    output [4:0] in,
    input [4:0] out
);
assign in = out;
endmodule

module mantle_wire__typeBit5 (
    input [4:0] in,
    output [4:0] out
);
assign out = in;
endmodule

module Main (
    input [4:0] I__0,
    input I__1,
    output [4:0] O__0,
    output O__1
);
wire [4:0] _$_U1_out;
wire [5:0] x;
mantle_wire__typeBit5 _$_U1 (
    .in(I__0),
    .out(_$_U1_out)
);
mantle_wire__typeBitIn5 _$_U2 (
    .in(O__0),
    .out(x[4:0])
);
assign x = {I__1,_$_U1_out[4:0]};
assign O__1 = x[5];
endmodule

