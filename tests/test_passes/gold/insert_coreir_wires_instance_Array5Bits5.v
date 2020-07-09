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
    input [4:0] I_0,
    input [4:0] I_1,
    input [4:0] I_2,
    input [4:0] I_3,
    input [4:0] I_4,
    output [4:0] O_0,
    output [4:0] O_1,
    output [4:0] O_2,
    output [4:0] O_3,
    output [4:0] O_4
);
wire [4:0] Foo_inst0_O_0;
wire [4:0] Foo_inst0_O_1;
wire [4:0] Foo_inst0_O_2;
wire [4:0] Foo_inst0_O_3;
wire [4:0] Foo_inst0_O_4;
wire [4:0] _$_U1_out;
wire [4:0] _$_U2_out;
wire [4:0] _$_U3_out;
wire [4:0] _$_U4_out;
wire [4:0] _$_U5_out;
wire [24:0] x;
Foo Foo_inst0 (
    .I_0(I_0),
    .I_1(I_1),
    .I_2(I_2),
    .I_3(I_3),
    .I_4(I_4),
    .O_0(Foo_inst0_O_0),
    .O_1(Foo_inst0_O_1),
    .O_2(Foo_inst0_O_2),
    .O_3(Foo_inst0_O_3),
    .O_4(Foo_inst0_O_4)
);
mantle_wire__typeBit5 _$_U1 (
    .in(Foo_inst0_O_0),
    .out(_$_U1_out)
);
mantle_wire__typeBitIn5 _$_U10 (
    .in(O_3),
    .out(x[19:15])
);
mantle_wire__typeBitIn5 _$_U11 (
    .in(O_4),
    .out(x[24:20])
);
mantle_wire__typeBit5 _$_U2 (
    .in(Foo_inst0_O_1),
    .out(_$_U2_out)
);
mantle_wire__typeBit5 _$_U3 (
    .in(Foo_inst0_O_2),
    .out(_$_U3_out)
);
mantle_wire__typeBit5 _$_U4 (
    .in(Foo_inst0_O_3),
    .out(_$_U4_out)
);
mantle_wire__typeBit5 _$_U5 (
    .in(Foo_inst0_O_4),
    .out(_$_U5_out)
);
mantle_wire__typeBitIn5 _$_U7 (
    .in(O_0),
    .out(x[4:0])
);
mantle_wire__typeBitIn5 _$_U8 (
    .in(O_1),
    .out(x[9:5])
);
mantle_wire__typeBitIn5 _$_U9 (
    .in(O_2),
    .out(x[14:10])
);
assign x = {_$_U5_out[4:0],_$_U4_out[4:0],_$_U3_out[4:0],_$_U2_out[4:0],_$_U1_out[4:0]};
endmodule

