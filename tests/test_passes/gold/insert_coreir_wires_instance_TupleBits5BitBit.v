// Module `Foo` defined externally
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
wire [4:0] Foo_inst0_O__0;
wire Foo_inst0_O__1;
wire [4:0] _$0_out;
wire [5:0] x;
Foo Foo_inst0 (
    .I__0(I__0),
    .I__1(I__1),
    .O__0(Foo_inst0_O__0),
    .O__1(Foo_inst0_O__1)
);
mantle_wire__typeBit5 _$0 (
    .in(Foo_inst0_O__0),
    .out(_$0_out)
);
mantle_wire__typeBitIn5 _$1 (
    .in(O__0),
    .out(x[4:0])
);
assign x = {Foo_inst0_O__1,_$0_out[4:0]};
assign O__1 = x[5];
endmodule

